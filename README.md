
-----

# 💗 Extractor de Texto OCR - Green & Pink Edition 💚

**Una aplicación de escritorio diseñada para extraer de forma inteligente el texto resaltado en tus imágenes y documentos escaneados.**

[Aquí va una captura de pantalla o GIF de la aplicación]

-----

## ✨ Características Principales

  * **🔍 OCR por Color:** Extrae texto específicamente de áreas resaltadas en **amarillo, verde, rosa o violeta**.
  * **📂 Procesamiento por Lotes:** Arrastra una carpeta completa para analizar múltiples imágenes de una sola vez.
  * **🖼️ Interfaz Intuitiva:** Arrastra y suelta imágenes directamente en la aplicación para una vista previa instantánea.
  * **✍️ Limpieza de Texto:** Incluye una herramienta para eliminar saltos de línea innecesarios y formatear el texto extraído con un solo clic.
  * **💾 Exportación Fácil:** Copia el texto al portapapeles o guarda los resultados individualmente o todos a la vez en archivos `.txt`.
  * **🎨 Estilo Único:** Una interfaz personalizada "Green & Pink" con una barra de título manejable y tooltips de ayuda.

-----

## 📋 Requisitos (¡Importante\!)

Para que la aplicación funcione, necesitas tener **Tesseract OCR** instalado en tu sistema o disponible junto al ejecutable.

#### Opción 1 (Recomendada): Incluir Tesseract con la App

1.  Descarga la versión portable de Tesseract para Windows desde [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2.  Descomprime el archivo y renombra la carpeta a `Tesseract-OCR`.
3.  Copia esta carpeta `Tesseract-OCR` y pégala **en el mismo directorio donde está el `ExtractorOCR.exe`**.

#### Opción 2: Instalación en Windows

1.  Instala Tesseract OCR usando el instalador oficial.
2.  Asegúrate de que la ruta de instalación (`C:\Program Files\Tesseract-OCR`) esté accesible.

-----

## 🚀 Cómo Usar

1.  Descarga la última versión del `.exe` desde la sección de **[Releases](https://www.google.com/search?q=https://github.com/martin-ratti/Extractor-OCR-Python/releases)** de este repositorio.
2.  Asegúrate de cumplir con los **Requisitos** mencionados arriba.
3.  Ejecuta `ExtractorOCR.exe`.
4.  Arrastra una imagen o una carpeta a la ventana.
5.  Selecciona el color del resaltador que quieres detectar.
6.  Haz clic en **"Extraer Texto"**. Los resultados aparecerán en la lista de la derecha.
7.  Usa los botones de acción para limpiar, copiar o guardar el texto.

-----

## 🛠️ Para Desarrolladores (Compilar desde la Fuente)

Si deseas modificar o compilar el proyecto tú mismo, sigue estos pasos:

### 1\. Clona el repositorio

```bash
git clone https://github.com/martin-ratti/Extractor-OCR-Python.git
cd Extractor-OCR-Python
```

### 2\. Crea y activa un entorno virtual

```bash
python -m venv venv

# En Windows (CMD/PowerShell)
.\venv\Scripts\Activate

# En macOS/Linux (Bash/Zsh)
source venv/bin/activate
```

### 3\. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4\. Ejecuta la aplicación

```bash
python main.py
```

### 5\. Compila el ejecutable (One-File)

El siguiente comando empaqueta la aplicación en un solo `.exe`. Asume que tienes una carpeta `assets/` con tus iconos en la raíz del proyecto.

```bash
# En Windows (usa ; como separador)
pyinstaller --onefile --noconsole --name ExtractorOCR --add-data "assets;assets" main.py

# En macOS/Linux (usa : como separador)
pyinstaller --onefile --noconsole --name ExtractorOCR --add-data "assets:assets" main.py
```

> **Nota:** Para que la versión compilada funcione, recuerda colocar la carpeta `Tesseract-OCR` junto al `.exe` generado en la carpeta `dist/`.

-----

## 🧩 Tecnologías Utilizadas

  * **Python 🐍**
  * **CustomTkinter** y **TkinterDnD2** para la interfaz gráfica.
  * **OpenCV** para el procesamiento de imágenes y detección de color.
  * **Pytesseract (Tesseract)** como motor de OCR.
  * **Pillow** para el manejo de imágenes.
  * **PyInstaller** para el empaquetado.

-----

## 📜 Licencia

Este proyecto puedes usarlo, modificarlo y distribuirlo libremente, siempre citando la autoría correspondiente.

-----
