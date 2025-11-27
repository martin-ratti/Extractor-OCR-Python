<div align="center">

# 💗 Extractor de Texto OCR - Green & Pink 💚

<img src="https://img.shields.io/badge/Estado-Estable-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-2.0.0-blue?style=for-the-badge" alt="Version Badge"/>
<img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="License Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Arquitectura-Clean%20Arch-orange?style=for-the-badge&logo=expertsexchange&logoColor=white" alt="Clean Arch Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/CV-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV Badge"/>
    <img src="https://img.shields.io/badge/OCR-Tesseract-blue?style=for-the-badge&logo=googlelens&logoColor=white" alt="Tesseract Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

El **Extractor de Texto OCR** es una herramienta de escritorio profesional diseñada para automatizar la digitalización de información selectiva. A diferencia de los OCR tradicionales que escanean toda la página, esta herramienta utiliza visión artificial para detectar y extraer texto **únicamente de las áreas resaltadas**.

Ideal para estudiantes, investigadores y abogados que trabajan con documentos físicos marcados con resaltadores estándar.

> **Colores Soportados:** 🟨 Amarillo | 🟩 Verde | 🌸 Rosa | 🟣 Violeta

---

## 🏛️ Arquitectura y Diseño (Clean Architecture)

Este proyecto no es solo un script; está construido siguiendo estrictamente los principios de **Clean Architecture** y **SOLID**, garantizando que la lógica de negocio sea independiente de la interfaz gráfica y de las librerías externas.

### Diagrama de Capas

| Capa | Ruta | Responsabilidad |
| :--- | :--- | :--- |
| **Interface** | `src/interface/gui.py` | **Presentación:** Maneja la ventana, eventos *Drag & Drop*, hilos de ejecución y feedback visual. No conoce la lógica del OCR. |
| **Core** | `src/core/use_cases.py` | **Dominio:** Define *qué* debe hacer el sistema (Casos de Uso) y los *Protocolos* (Interfaces) que debe cumplir la infraestructura. Es Python puro. |
| **Infrastructure** | `src/infrastructure/ocr_service.py` | **Implementación:** Contiene la "suciedad" técnica: OpenCV, máscaras de color HSV y llamadas a binarios de Tesseract. |

-----

## 🚀 Características Principales

  * **🔍 Algoritmo de Visión Artificial:** Utiliza rangos HSV específicos para crear máscaras binarias que aíslan el texto resaltado del resto del documento.
  * **🎨 UI "Green & Pink":** Interfaz moderna basada en `CustomTkinter` con modo claro, tooltips nativos y feedback de progreso.
  * **🖱️ Drag & Drop Nativo:** Soporte completo mediante `TkinterDnD` para arrastrar archivos o carpetas enteras.
  * **⚡ Procesamiento por Lotes (Multithreading):** La interfaz no se congela al procesar carpetas grandes gracias al manejo de hilos y colas de eventos.
  * **🛠️ Herramientas de Post-Procesado:**
      * **Limpieza Inteligente:** Algoritmo para reconstruir párrafos rotos por el OCR.
      * **Auto-detect Tesseract:** El sistema busca automáticamente el binario de Tesseract en rutas comunes y relativas.

-----

## 📋 Requisito Crítico: Tesseract OCR

> ⚠️ **Atención:** Esta aplicación requiere el motor **Tesseract OCR** para interpretar los caracteres.

### Opción A: Modo Portable (Recomendado ⭐)

Esta opción hace que la app sea totalmente portable (USB, Nube, etc).

1.  Descarga **Tesseract Portable** (v5.x o superior).
2.  Extrae el contenido y renombra la carpeta a `Tesseract-OCR`.
3.  Coloca dicha carpeta **en el mismo directorio** donde está `ExtractorOCR.exe`.

### Opción B: Instalación en Sistema

1.  Instala Tesseract en Windows ([Instalador Oficial UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)).
2.  La aplicación buscará automáticamente en:
      * `C:\Program Files\Tesseract-OCR\tesseract.exe`
      * `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`

-----

## 🛠️ Modo de Uso

```text
/Tu Carpeta
├── ExtractorOCR.exe         <-- Ejecutable
├── assets/                  <-- Iconos (Requerido)
└── Tesseract-OCR/           <-- Motor OCR (Opcional si está instalado en sistema)
```

1.  **Abrir:** Ejecuta la aplicación.
2.  **Cargar:** Arrastra una imagen o selecciona una carpeta completa.
3.  **Configurar:** Elige el color del resaltador que usaste en el papel (ej. "Amarillo").
4.  **Extraer:** Pulsa el botón y espera a que la barra de progreso termine.
5.  **Exportar:** Puedes copiar al portapapeles o guardar en `.txt` masivamente.

-----

## ❓ Solución de Problemas (Troubleshooting)

**Error: "No se encontró Tesseract"**

  * Verifica que la carpeta se llame exactamente `Tesseract-OCR`.
  * Asegúrate de que dentro de esa carpeta exista el archivo `tesseract.exe`.

**El texto sale "basura" o caracteres extraños**

  * Asegúrate de que la iluminación de la foto sea uniforme.
  * El resaltador debe tener buen contraste. Los colores muy oscuros o fotos con sombras fuertes dificultan la creación de la máscara HSV.

-----

## 🧑‍💻 Setup para Desarrolladores

Si deseas contribuir o modificar el código:

### 1\. Configuración del Entorno

```bash
# Clonar repositorio
git clone [https://github.com/martin-ratti/Extractor-OCR-Python.git](https://github.com/martin-ratti/Extractor-OCR-Python.git)

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2\. Ejecución en Dev

```bash
python main.py
```

### 3\. Compilación (.exe)

El proyecto incluye assets (imágenes). Asegúrate de incluirlos en la compilación:

```bash
pyinstaller --onefile --noconsole --name ExtractorOCR --add-data "assets;assets" --icon="assets/icon.ico" main.py
```

-----

## ⚖️ Créditos

Desarrollado por **Martín Ratti**.

  * Iconos por [Flaticon](https://www.flaticon.com).
  * Librerías: OpenCV, PyTesseract, CustomTkinter.

