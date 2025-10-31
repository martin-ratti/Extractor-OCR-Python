# main.py
"""
Punto de entrada principal de la aplicación OCR.

Este script inicializa y ejecuta la interfaz de usuario.
"""

from src.interface import gui

# Comprobación estándar para asegurar que el script se ejecuta directamente
if __name__ == "__main__":
    # Inicia la interfaz gráfica de usuario
    gui.main()