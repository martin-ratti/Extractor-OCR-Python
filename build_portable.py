import os
import shutil
import PyInstaller.__main__
import zipfile

def build():
    print("🚀 Iniciando construcción de versión portable...")

    # 1. Limpiar builds anteriores
    if os.path.exists("dist"): shutil.rmtree("dist")
    if os.path.exists("build"): shutil.rmtree("build")

    # 2. Ejecutar PyInstaller
    # --onedir: Crea una carpeta (más fácil para depurar y añadir dependencias)
    # --noconsole: Sin ventana de consola negra
    # --name: Nombre del ejecutable
    # --collect-all: Asegurar que customtkinter y tkinterdnd2 se incluyan completos
    print("🔨 Compilando ejecutable...")
    PyInstaller.__main__.run([
        'main.py',
        '--name=MoraExtractor',
        '--onedir',
        '--noconsole',
        '--clean',
        '--collect-all=customtkinter',
        '--collect-all=tkinterdnd2',
        '--icon=assets/app_icon.png' if os.path.exists('assets/app_icon.png') else '--name=MoraExtractor' 
    ])

    dist_folder = os.path.join("dist", "MoraExtractor")
    portable_folder_name = "Mora_Extractor_Portable"
    portable_path = os.path.join("dist", portable_folder_name)
    
    # Renombrar la carpeta de salida a algo más amigable
    if os.path.exists(portable_path): shutil.rmtree(portable_path)
    os.rename(dist_folder, portable_path)

    print("📂 Copiando dependencias...")

    # 3. Copiar carpeta Tesseract-OCR
    # Intentar copiar desde Program Files si existe, o desde local
    tesseract_sys_path = r"C:\Program Files\Tesseract-OCR"
    tesseract_dest_path = os.path.join(portable_path, "Tesseract-OCR")
    
    if os.path.exists(tesseract_sys_path):
        print(f"   -> Copiando Tesseract desde {tesseract_sys_path}...")
        shutil.copytree(tesseract_sys_path, tesseract_dest_path)
    else:
        print("⚠️ NO se encontró Tesseract en C:\\Program Files\\Tesseract-OCR. Asegúrate de copiarlo manualmente.")

    # 4. Copiar carpeta assets
    assets_src = "assets"
    assets_dest = os.path.join(portable_path, "assets")
    if os.path.exists(assets_src):
        print("   -> Copiando assets...")
        shutil.copytree(assets_src, assets_dest)
    else:
        print("⚠️ Carpeta assets no encontrada.")

    # 5. Crear ZIP
    print("📦 Creando archivo ZIP...")
    zip_filename = "Mora_Extractor_Portable.zip"
    zip_path = os.path.join("dist", zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "dist")
                zipf.write(file_path, arcname)

    print(f"\n✅ ¡Éxito! Archivo portable creado en: {os.path.abspath(zip_path)}")

if __name__ == "__main__":
    build()
