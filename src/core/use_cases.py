"""
Módulo que contiene los casos de uso o la lógica de negocio principal.
Es agnóstico a la implementación concreta de la infraestructura o la interfaz.
"""
from typing import Protocol

# --- Definición de la Interfaz del Servicio de OCR ---
class OcrServiceProtocol(Protocol):
    """Define el contrato que cualquier servicio de OCR debe cumplir."""
    def extract_text_from_image(self, image_path: str, color: str) -> str:
        ...

# --- Caso de Uso: Extracción de Texto ---
def extraer_texto_de_imagen(ocr_service: OcrServiceProtocol, image_path: str, color: str) -> str:
    """
    Orquesta la extracción de texto de una imagen.

    Args:
        ocr_service: Una implementación del servicio de OCR.
        image_path: La ruta al archivo de imagen.
        color: El color del resaltador a buscar.

    Returns:
        El texto extraído de la imagen.
    """
    if not image_path:
        return "Error: No se proporcionó una ruta de imagen."

    # Delega la extracción de texto al servicio de infraestructura.
    texto_extraido = ocr_service.extract_text_from_image(image_path, color)

    return texto_extraido

