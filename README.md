<h1 align="center">💗 Extractor de Texto OCR - Green & Pink 💚</h1>

<div align="center">
    <img src="https://img.shields.io/badge/Estado-Estable-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
    <img src="https://img.shields.io/badge/Versión-2.0.0-blue?style=for-the-badge" alt="Version Badge"/>
</div>

<p align="center">
    <a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
        <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/CV-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV Badge"/>
    <img src="https://img.shields.io/badge/OCR-Tesseract-blue?style=for-the-badge&logo=googlelens&logoColor=white" alt="Tesseract Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
</p>

<hr>

<h2>🎯 Objetivo y Alcance</h2>

<p>
    El <strong>Extractor de Texto OCR</strong> es una herramienta de escritorio diseñada para automatizar la digitalización de información. 
    Su función principal es detectar y extraer texto específicamente de <strong>áreas resaltadas</strong> en documentos o imágenes escaneadas.
</p>

<p>
    Ideal para estudiantes y profesionales que necesitan procesar apuntes, libros o informes. La aplicación combina la potencia de 
    <strong>Tesseract OCR</strong> con procesamiento de imágenes avanzado mediante <strong>OpenCV</strong>, todo envuelto en una interfaz moderna y amigable.
</p>

<hr>

<h2>⚙️ Stack Tecnológico & Arquitectura</h2>

<p>El proyecto sigue los principios de <strong>Clean Architecture</strong> para separar la lógica de procesamiento de la interfaz visual.</p>

<table>
 <thead>
  <tr>
   <th>Capa / Componente</th>
   <th>Tecnología / Ruta</th>
   <th>Descripción</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><strong>Interface (GUI)</strong></td>
   <td><code>src/interface/</code><br>(CustomTkinter + TkinterDnD)</td>
   <td>Interfaz moderna "Green & Pink". Soporta <em>Drag & Drop</em> de archivos y carpetas, visualización de imágenes y edición de texto.</td>
  </tr>
  <tr>
   <td><strong>Core (Lógica)</strong></td>
   <td><code>src/core/</code></td>
   <td>Define los protocolos y casos de uso para la extracción, independiente de la librería OCR usada.</td>
  </tr>
  <tr>
   <td><strong>Infrastructure</strong></td>
   <td><code>src/infrastructure/</code><br>(OpenCV + Pytesseract)</td>
   <td>Implementación concreta del OCR. Aplica filtros HSV para detectar colores (Amarillo, Verde, Rosa, Violeta) y máscaras binarias.</td>
  </tr>
  <tr>
   <td><strong>Empaquetado</strong></td>
   <td>PyInstaller</td>
   <td>Generación del ejecutable <code>.exe</code> portable con assets incrustados.</td>
  </tr>
 </tbody>
</table>

<hr>

<h2>🚀 Características Principales</h2>

<ul>
    <li><strong>🔍 OCR Inteligente por Color</strong>: Algoritmo capaz de aislar y extraer texto resaltado en <strong>Amarillo, Verde, Rosa o Violeta</strong>.</li>
    <li><strong>📂 Procesamiento por Lotes</strong>: Arrastra una carpeta entera para analizar múltiples imágenes automáticamente.</li>
    <li><strong>✍️ Herramientas de Edición</strong>:
        <ul>
            <li><strong>Limpieza:</strong> Elimina saltos de línea erróneos típicos del OCR.</li>
            <li><strong>Copia Rápida:</strong> Copia el resultado al portapapeles con un clic.</li>
        </ul>
    </li>
    <li><strong>🖼️ Previsualización Dinámica</strong>: Visualiza la imagen cargada y limpia la selección fácilmente.</li>
    <li><strong>💾 Exportación Flexible</strong>: Guarda los resultados en <code>.txt</code> individualmente o de forma masiva.</li>
</ul>

<hr>

<h2>📋 Requisito Crítico: Tesseract OCR</h2>

<p>Para que la aplicación funcione, el motor <strong>Tesseract OCR</strong> debe estar disponible. Tienes dos opciones:</p>

<h3>Opción A: Modo Portable (Recomendado)</h3>
<ol>
    <li>Descarga Tesseract Portable desde <a href="https://github.com/UB-Mannheim/tesseract/wiki">UB Mannheim</a>.</li>
    <li>Descomprime y renombra la carpeta a <code>Tesseract-OCR</code>.</li>
    <li>Coloca esa carpeta <strong>en el mismo directorio</strong> donde esté el archivo <code>ExtractorOCR.exe</code> (o <code>main.py</code>).</li>
</ol>

<h3>Opción B: Instalación en Sistema</h3>
<ol>
    <li>Instala Tesseract en Windows mediante el instalador oficial.</li>
    <li>La aplicación buscará automáticamente en rutas estándar como <code>C:\Program Files\Tesseract-OCR</code>.</li>
</ol>

<hr>

<h2>🛠️ Modo de Uso</h2>

<pre>
/Tu Carpeta
├── ExtractorOCR.exe         <-- La aplicación
└── Tesseract-OCR/           <-- Carpeta del motor OCR (Opción A)
</pre>

<ol>
    <li><strong>Iniciar:</strong> Ejecuta <code>ExtractorOCR.exe</code>.</li>
    <li><strong>Cargar:</strong> Arrastra una imagen o carpeta a la ventana principal.</li>
    <li><strong>Configurar:</strong> Selecciona el color del resaltador (ej. "Amarillo") en el menú superior.</li>
    <li><strong>Procesar:</strong> Haz clic en <strong>"Extraer Texto"</strong>.</li>
    <li><strong>Gestionar:</strong> Usa los botones laterales para limpiar el formato, copiar o guardar el texto extraído.</li>
</ol>

<hr>

<h2>🧑‍💻 Setup para Desarrolladores</h2>

Si deseas modificar el código o compilar tu propia versión:

<h3>1. Configuración del Entorno</h3>
<pre><code># Clonar repositorio
git clone https://github.com/martin-ratti/Extractor-OCR-Python.git

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
</code></pre>

<h3>2. Ejecución</h3>
<pre><code>python main.py</code></pre>

<h3>3. Compilación (.exe)</h3>
<p>Comando para generar el ejecutable <em>single-file</em> (asegúrate de tener la carpeta <code>assets</code>):</p>
<pre><code>pyinstaller --onefile --noconsole --name ExtractorOCR --add-data "assets;assets" main.py</code></pre>

<hr>

<h2>⚖️ Créditos</h2>

<p>
    Desarrollado por <strong>Martín Ratti</strong>. Proyecto de código abierto para facilitar la digitalización de documentos.
</p>
