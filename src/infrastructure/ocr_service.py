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
        # Rango HSV de cada color de resaltador
        # HSV: Hue (0-180), Saturation (0-255), Value (0-255)
        # Rangos calibrados para ser EXCLUSIVOS y evitar solapamientos.
        # Saturation Min subido a 50 para ignorar sombras grises y blancos sucios.
        self.color_ranges: ColorRange = {
            # Naranja: 0-18 (Antes 0-25)
            "naranja": (np.array([0, 50, 80]), np.array([18, 255, 255])),
            # Amarillo: 19-35 (Antes 22-45, evitando verde)
            "amarillo": (np.array([19, 50, 120]), np.array([35, 255, 255])),
            # Verde: 36-90 (Antes 35-85, rango principal)
            "verde": (np.array([36, 50, 120]), np.array([90, 255, 255])),
            # Celeste: 91-110
            "celeste": (np.array([91, 50, 120]), np.array([110, 255, 255])),
            # Azul: 111-125
            "azul": (np.array([111, 50, 120]), np.array([125, 255, 255])),
            # Violeta: 126-160
            "violeta": (np.array([126, 50, 120]), np.array([160, 255, 255])),
            # Rosa: 161-180
            "rosa": (np.array([161, 50, 120]), np.array([180, 255, 255])),
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

    def correct_orientation(self, image: np.ndarray) -> np.ndarray:
        """
        Detecta la orientación de la imagen y la rota si es necesario.
        """
        try:
            # Usamos Tesseract OSD (Orientation and Script Detection)
            # image_to_osd devuelve info como: "Rotate: 90\nOrientation in degrees: 90\n..."
            osd_data = pytesseract.image_to_osd(image)
            
            rotation_angle = 0
            # Parsear la salida texto de OSD
            for line in osd_data.splitlines():
                if "Rotate:" in line:
                    rotation_angle = int(line.split(":")[1].strip())
                    break
            
            if rotation_angle == 0:
                return image

            print(f"🔄 Auto-rotación detectada: {rotation_angle}°")

            # Rotar la imagen según el ángulo detectado
            if rotation_angle == 90:
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            elif rotation_angle == 180:
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif rotation_angle == 270:
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
            return image

        except Exception as e:
            # Si falla OSD (ej. imagen sin suficiente texto para detectar orientación),
            # devolvemos la original sin cambios.
            # print(f"Info: No se pudo detectar orientación ({e})")
            return image

    def detect_active_colors(self, image: np.ndarray) -> list[str]:
        """
        Analiza la imagen para determinar qué colores de resaltado están presentes.
        Usa un umbral dinámico basado en el tamaño de la imagen y un umbral relativo
        para filtrar falsos positivos (ruido).
        """
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        height, width, _ = image.shape
        total_pixels = height * width
        
        # Umbral 1: Área mínima absoluta (0.2% de la imagen)
        # Para una foto de 12MP (4000x3000), esto es ~24,000 píxeles.
        # Para 720p (1280x720), esto es ~1,800 píxeles.
        MIN_AREA_PERCENT = 0.002 
        min_pixels_absolute = int(total_pixels * MIN_AREA_PERCENT) # Aumentamos umbral significativamente

        detected_stats = {}

        for color_name, (lower, upper) in self.color_ranges.items():
            mask = cv2.inRange(hsv_image, lower, upper)
            
            # Dilatar máscara para conectar puntos dispersos antes de contar
            # Revertido a solo dilatación simple para no perder detalles finos
            kernel = np.ones((5,5), np.uint8)
            # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) # ELIMINADO: Comía demasiado texto
            mask = cv2.dilate(mask, kernel, iterations=2)

            count = cv2.countNonZero(mask)
            
            if count > min_pixels_absolute:
                detected_stats[color_name] = count
        
        if not detected_stats:
            return []

        # Umbral 2: Relativo al color dominante
        # Si el verde tiene 100,000 px y el violeta (sombra) tiene 5,000, ignoramos el violeta.
        max_pixels = max(detected_stats.values())
        RELATIVE_THRESHOLD = 0.20 # Debe tener al menos el 20% de píxeles del color dominante
        
        final_colors = []
        for color, count in detected_stats.items():
            if count >= max_pixels * RELATIVE_THRESHOLD:
                final_colors.append(color)
            elif self.DEBUG:
                print(f"⚠️ Color '{color}' descartado por ser minoritario ({count} px vs {max_pixels} px)")

        return final_colors

    def extract_text_from_image(self, image_path: str, color: str = "auto") -> str:
        """
        Método ÚNICO de extracción inteligente.
        1. Intenta detectar colores de resaltado.
        2. Si encuentra colores, extrae el texto de esas zonas.
        3. Si NO encuentra colores, escanea toda la página con estrategia robusta (Smart Fallback).
        """
        try:
            # image = cv2.imread(image_path) # Reemplazado por versión safe para unicode
            image = self._read_image_safe(image_path)
            
            if image is None:
                # Intento de debug adicional: verificar si el archivo existe
                if not os.path.exists(image_path):
                     return f"Error: No se encuentra el archivo en la ruta: {image_path}"
                return "Error: No se pudo cargar la imagen (formato no soportado o ruta inválida)."

            # --- Corregir orientación ---
            image = self.correct_orientation(image)
            # ---------------------------

            # Paso 1: Intentar detección de colores (Modo Resaltador)
            active_colors = self.detect_active_colors(image)
            
            if active_colors:
                text_from_colors = self._extract_highlighted_text(image, active_colors)
                if text_from_colors:
                    return text_from_colors
                # Si detectó colores pero no pudo leer texto, caer al fallback
                if self.DEBUG: print("⚠️ Colores detectados pero sin texto legible. Intentando escaneo completo...")

            # Paso 2: Fallback a Escaneo Completo (Modo "Sin Filtro" Robusto)
            return self._extract_full_page_robust(image)

        except Exception as e:
            return f"Ocurrió un error considerable durante el OCR: {e}"

    def _extract_highlighted_text(self, image: np.ndarray, active_colors: list) -> str:
        """Extrae texto solo de las zonas de los colores especificados."""
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)
        
        kernel_connect = np.ones((3, 15), np.uint8) # Para conectar letras horizontalmente
        kernel_clean = np.ones((5, 5), np.uint8)    # Para eliminar ruido

        config = '-l spa+eng --psm 6'

        final_output = []
        for color_name in active_colors:
            lower, upper = self.color_ranges[color_name]
            mask = cv2.inRange(hsv_image, lower, upper)
            
            # 1. Limpieza de ruido ELIMINADA para recuperar calidad de texto
            # cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_clean)
            
            # 2. Solo Dilatación para cubrir letras (usamos la mask original)
            dilated_mask = cv2.dilate(mask, kernel_connect, iterations=3)
            
            final_image_part = cv2.bitwise_and(thresh_image, thresh_image, mask=dilated_mask)
            
            text_part = pytesseract.image_to_string(final_image_part, config=config).strip()
            
            # Filtrar basura muy corta (menos de 3 letras suele ser ruido)
            if text_part and len(text_part) > 3:
                header = f"{color_name.upper()}:"
                final_output.append(f"{header}\n\n{text_part}")
        
        if final_output:
            return "\n\n" + ("-"*30) + "\n\n".join(final_output)
        return ""

    def _extract_full_page_robust(self, image: np.ndarray) -> str:
        """Intenta leer la página completa usando múltiples estrategias de pre-procesamiento."""
        configs_to_try = [
            # Intento 1: Pre-procesamiento AVANZADO (Mejor para sombras/curvatura)
            ("Avanzado", lambda img: self._preprocess_advanced(img), '-l spa+eng --psm 3'),
            # Intento 2: Pre-procesamiento MÍNIMO (Mejor para luz uniforme)
            ("Mínimo", lambda img: self._preprocess_minimal(img), '-l spa+eng --psm 3'),
            # Intento 3: Raw (Sin tocar)
            ("Raw", lambda img: img, '-l spa+eng --psm 3'),
             # Intento 4: PSM 6 Fallback
            ("Bloque", lambda img: self._preprocess_minimal(img), '-l spa+eng --psm 6')
        ]

        for name, preprocess_func, cfg in configs_to_try:
            try:
                processed_img = preprocess_func(image)
                text = pytesseract.image_to_string(processed_img, config=cfg).strip()
                if len(text) > 15: # Umbral mínimo de éxito
                    if self.DEBUG: print(f"✅ Éxito con estrategia: {name}")
                    return text
            except Exception as e:
                if self.DEBUG: print(f"⚠️ Falló estrategia {name}: {e}")
                continue
        
        return "No se encontró texto legible en la imagen (Intento fallido en todos los modos)."

    def _preprocess_advanced(self, image):
        """CLAHE + Denoise + Adaptive Threshold"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return binary

    def _preprocess_minimal(self, image):
        """Grayscale + Slight Blur"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray, (3, 3), 0)

    def _read_image_safe(self, path: str) -> np.ndarray:
        """
        Lee una imagen soportando rutas con caracteres Unicode/especiales en Windows.
        cv2.imread falla silenciosamente con rutas que tienen acentos o caracteres no ASCII.
        """
        try:
            # np.fromfile lee el archivo binario sin importar el nombre
            stream = np.fromfile(path, dtype=np.uint8)
            # cv2.imdecode decodifica el buffer de memoria a imagen OpenCV
            image = cv2.imdecode(stream, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            if self.DEBUG: print(f"Error en _read_image_safe: {e}")
            return None


