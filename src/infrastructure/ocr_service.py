"""
Módulo de infraestructura que implementa el servicio de OCR
con detección de color de resaltador para múltiples colores.
"""
import cv2
import numpy as np
import pytesseract
import os
from typing import Protocol, Dict, Tuple

# --- Tipos de Datos ---
ColorRange = Dict[str, Tuple[np.ndarray, np.ndarray]]

# --- Protocolo ---
class OcrServiceProtocol(Protocol):
    """Define el contrato que cualquier servicio de OCR debe cumplir."""
    def extract_text_from_image(self, image_path: str, color: str) -> str:
        ...


# --- Implementación Concreta ---
class OcrService:
    """
    Servicio OCR que detecta texto en zonas resaltadas con color.
    Incluye detección automática del ejecutable de Tesseract.
    """
    DEBUG = False

    def __init__(self):
        # Rango HSV de cada color de resaltador
        self.color_ranges: ColorRange = {
            "amarillo": (np.array([15, 40, 60]), np.array([40, 255, 255])),
            "verde": (np.array([40, 40, 40]), np.array([80, 255, 255])),
            "rosa": (np.array([145, 60, 100]), np.array([175, 255, 255])),
            "violeta": (np.array([125, 50, 50]), np.array([145, 255, 255])),
        }

        # --- DETECCIÓN AUTOMÁTICA DE TESSERACT ---
        posibles_rutas = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.join(os.getcwd(), "Tesseract-OCR", "tesseract.exe"),
            os.path.join(os.path.dirname(__file__), "..", "..", "Tesseract-OCR", "tesseract.exe"),
        ]

        for ruta in posibles_rutas:
            ruta_absoluta = os.path.abspath(ruta)
            if os.path.exists(ruta_absoluta):
                pytesseract.pytesseract.tesseract_cmd = ruta_absoluta
                print(f"✅ Tesseract encontrado en: {ruta_absoluta}")
                break
        else:
            print("⚠️ No se encontró Tesseract. Coloca la carpeta 'Tesseract-OCR' junto al .exe o instálalo en Windows.")

    def extract_text_from_image(self, image_path: str, color: str) -> str:
        """Extrae texto de una imagen resaltada con el color especificado."""
        lower_bound, upper_bound = self.color_ranges.get(color, (None, None))
        if lower_bound is None:
            return f"Error: Color '{color}' no soportado."

        try:
            image = cv2.imread(image_path)
            if image is None:
                return "Error: No se pudo cargar la imagen."

            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
            if self.DEBUG: cv2.imwrite(f"_debug_01_mask_{color}.png", mask)

            kernel = np.ones((3, 15), np.uint8)
            dilated_mask = cv2.dilate(mask, kernel, iterations=3)
            if self.DEBUG: cv2.imwrite(f"_debug_02_dilated_mask_{color}.png", dilated_mask)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)
            final_image = cv2.bitwise_and(thresh_image, thresh_image, mask=dilated_mask)
            if self.DEBUG: cv2.imwrite(f"_debug_03_final_image_{color}.png", final_image)

            config = '-l spa+eng --psm 6'
            texto_extraido = pytesseract.image_to_string(final_image, config=config)

            return texto_extraido.strip() or "No se encontró texto en las áreas resaltadas."

        except Exception as e:
            return f"Ocurrió un error durante el OCR: {e}"
