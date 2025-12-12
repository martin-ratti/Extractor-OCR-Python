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
    DEBUG = False  # Modo de prueba desactivado para producción

    def __init__(self):
        # Rango HSV de cada color de resaltador
        # HSV: Hue (0-180), Saturation (0-255), Value (0-255)
        # Rangos calibrados basados en análisis de imágenes reales de documentos
        self.color_ranges: ColorRange = {
            # Amarillo: Hue 22-38 (pico detectado en 30-40), separado de verde
            "amarillo": (np.array([22, 25, 120]), np.array([38, 255, 255])),
            # Verde: Hue 38-70 (pico detectado en 40-50), incluye verde lima
            "verde": (np.array([38, 25, 120]), np.array([70, 255, 255])),
            # Celeste/Turquesa: Hue 70-100, para resaltadores celestes/turquesa
            "celeste": (np.array([70, 25, 120]), np.array([100, 255, 255])),
            # Azul: Hue 100-120, para resaltadores azules
            "azul": (np.array([100, 25, 120]), np.array([120, 255, 255])),
            # Violeta: Hue 120-155, para resaltadores violeta/morado
            "violeta": (np.array([120, 25, 120]), np.array([155, 255, 255])),
            # Rosa: Hue 155-180 (pico detectado en 170-180), para rosas/magentas
            "rosa": (np.array([155, 25, 120]), np.array([180, 255, 255])),
            # Naranja: Hue 0-22 (pico detectado en 0-20), para naranja/salmón
            "naranja": (np.array([0, 25, 120]), np.array([22, 255, 255])),
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
