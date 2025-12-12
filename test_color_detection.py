# test_color_detection.py
"""
Script de prueba para analizar los colores HSV de las imagenes
y generar las mascaras de deteccion.
"""
import cv2
import numpy as np
import os

# Rangos de colores calibrados - separados para evitar solapamiento
color_ranges = {
    "amarillo": (np.array([22, 25, 120]), np.array([38, 255, 255])),
    "verde": (np.array([38, 25, 120]), np.array([70, 255, 255])),
    "rosa": (np.array([155, 25, 120]), np.array([180, 255, 255])),
    "violeta": (np.array([120, 25, 120]), np.array([155, 255, 255])),
    "naranja": (np.array([0, 25, 120]), np.array([22, 255, 255])),
}

# Directorio de imagenes de prueba
test_images_dir = "test_images"
output_dir = "debug_output"

# Crear directorio de salida
os.makedirs(output_dir, exist_ok=True)

def analyze_image(image_path, image_name):
    """Analiza una imagen y genera mascaras para cada color."""
    print(f"\n{'='*60}")
    print(f"Analizando: {image_name}")
    print(f"{'='*60}")
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: No se pudo cargar la imagen")
        return
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Para cada color, generar mascara
    best_color = None
    best_percentage = 0
    
    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv_image, lower, upper)
        
        # Contar pixeles detectados
        pixel_count = cv2.countNonZero(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        percentage = (pixel_count / total_pixels) * 100
        
        marker = " <<<" if percentage > best_percentage and percentage > 1 else ""
        if percentage > best_percentage and percentage > 1:
            best_color = color_name
            best_percentage = percentage
            
        print(f"  {color_name}: {pixel_count:,} pixeles ({percentage:.2f}%){marker}")
        
        # Guardar mascara si hay deteccion significativa (>0.5%)
        if percentage > 0.5:
            # Dilatar la mascara para visualizacion
            kernel = np.ones((3, 15), np.uint8)
            dilated_mask = cv2.dilate(mask, kernel, iterations=3)
            
            # Crear imagen con resaltado
            result = image.copy()
            result[dilated_mask > 0] = [0, 255, 0]  # Verde para el resaltado detectado
            
            output_file = os.path.join(output_dir, f"{image_name}_{color_name}_mask.png")
            cv2.imwrite(output_file, mask)
            
            output_file = os.path.join(output_dir, f"{image_name}_{color_name}_result.png")
            cv2.imwrite(output_file, result)
    
    if best_color:
        print(f"\n  MEJOR DETECCION: {best_color.upper()} ({best_percentage:.2f}%)")

def main():
    print("="*60)
    print("ANALISIS DE DETECCION DE COLORES EN IMAGENES DE PRUEBA")
    print("="*60)
    
    # Procesar todas las imagenes de prueba
    if os.path.exists(test_images_dir):
        for filename in sorted(os.listdir(test_images_dir)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_path = os.path.join(test_images_dir, filename)
                image_name = os.path.splitext(filename)[0]
                analyze_image(image_path, image_name)
    else:
        print(f"Error: No se encontro el directorio {test_images_dir}")
    
    print(f"\n{'='*60}")
    print("Analisis completado.")
    print("="*60)

if __name__ == "__main__":
    main()
