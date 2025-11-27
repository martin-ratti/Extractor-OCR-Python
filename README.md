<div align="center">

# 💗 Extractor de Texto OCR - Green & Pink 💚

<img src="https://img.shields.io/badge/Estado-Estable-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-2.0.0-blue?style=for-the-badge" alt="Version Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/CV-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV Badge"/>
    <img src="https://img.shields.io/badge/OCR-Tesseract-blue?style=for-the-badge&logo=googlelens&logoColor=white" alt="Tesseract Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

El **Extractor de Texto OCR** es una herramienta de escritorio diseñada para automatizar la digitalización de información. Su función principal es detectar y extraer texto específicamente de **áreas resaltadas** en documentos o imágenes escaneadas.

Ideal para estudiantes y profesionales que necesitan procesar apuntes, libros o informes. La aplicación combina la potencia de **Tesseract OCR** con procesamiento de imágenes avanzado mediante **OpenCV**, todo envuelto en una interfaz moderna y amigable.

---

## ⚙️ Stack Tecnológico & Arquitectura

El proyecto sigue los principios de **Clean Architecture** para separar la lógica de procesamiento de la interfaz visual.

| Capa / Componente | Tecnología / Ruta | Descripción |
| :--- | :--- | :--- |
| **Interface (GUI)** | `src/interface/`<br>_(CustomTkinter + TkinterDnD)_ | Interfaz moderna "Green & Pink". Soporta *Drag & Drop* de archivos y carpetas, visualización de imágenes y edición de texto. |
| **Core (Lógica)** | `src/core/` | Define los protocolos y casos de uso para la extracción, independiente de la librería OCR usada. |
| **Infrastructure** | `src/infrastructure/`<br>_(OpenCV + Pytesseract)_ | Implementación concreta del OCR. Aplica filtros HSV para detectar colores (Amarillo, Verde, Rosa, Violeta) y máscaras binarias. |
| **Empaquetado** | PyInstaller | Generación del ejecutable `.exe` portable con assets incrustados. |

---

## 🚀 Características Principales

* **🔍 OCR Inteligente por Color:** Algoritmo capaz de aislar y extraer texto resaltado en **Amarillo, Verde, Rosa o Violeta**.
* **📂 Procesamiento por Lotes:** Arrastra una carpeta entera para analizar múltiples imágenes automáticamente.
* **✍️ Herramientas de Edición:**
    * **Limpieza:** Elimina saltos de línea erróneos típicos del OCR.
    * **Copia Rápida:** Copia el resultado al portapapeles con un clic.
* **🖼️ Previsualización Dinámica:** Visualiza la imagen cargada y limpia la selección fácilmente.
* **💾 Exportación Flexible:** Guarda los resultados en `.txt` individualmente o de forma masiva.

---

## 📋 Requisito Crítico: Tesseract OCR

> ⚠️ **Atención:** Para que la aplicación funcione, el motor OCR debe estar presente.

### Opción A: Modo Portable (Recomendado)
Esta opción permite que la app funcione en cualquier PC sin instalaciones previas.
1.  Descarga Tesseract Portable desde [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2.  Descomprime y renombra la carpeta a `Tesseract-OCR`.
3.  Coloca esa carpeta **en el mismo directorio** donde esté el archivo `ExtractorOCR.exe` (o `main.py`).

### Opción B: Instalación en Sistema
1.  Instala Tesseract en Windows mediante el instalador oficial.
2.  La aplicación buscará automáticamente en rutas estándar como `C:\Program Files\Tesseract-OCR`.

---

## 🛠️ Modo de Uso

```text
/Tu Carpeta
├── ExtractorOCR.exe         <-- La aplicación
└── Tesseract-OCR/           <-- Carpeta del motor OCR (Opción A)
````

1.  **Iniciar:** Ejecuta `ExtractorOCR.exe`.
2.  **Cargar:** Arrastra una imagen o carpeta a la ventana principal.
3.  **Configurar:** Selecciona el color del resaltador (ej. "Amarillo") en el menú superior.
4.  **Procesar:** Haz clic en **"Extraer Texto"**.
5.  **Gestionar:** Usa los botones laterales para limpiar el formato, copiar o guardar el texto extraído.

-----

## 🧑‍💻 Setup para Desarrolladores

Si deseas modificar el código o compilar tu propia versión:

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

### 2\. Ejecución

```bash
python main.py
```

### 3\. Compilación (.exe)

Comando para generar el ejecutable *single-file* (asegúrate de tener la carpeta `assets`):

```bash
pyinstaller --onefile --noconsole --name ExtractorOCR --add-data "assets;assets" main.py
```

-----

## ⚖️ Créditos

Desarrollado por **Martín Ratti**. Proyecto de código abierto para facilitar la digitalización de documentos.
