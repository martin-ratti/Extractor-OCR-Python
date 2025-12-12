# analyze_hsv.py
"""
Script para analizar valores HSV en areas resaltadas de las imagenes.
"""
import cv2
import numpy as np
import os

test_images_dir = "test_images"

def analyze_hsv_distribution(image_path, image_name):
    """Analiza la distribucion de valores HSV en la imagen."""
    print(f"\n{'='*60}")
    print(f"Analizando HSV: {image_name}")
    print(f"{'='*60}")
    
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen")
        return
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    saturation = hsv[:,:,1]
    value = hsv[:,:,2]
    
    highlighter_mask = (saturation > 25) & (value > 100)
    
    if np.sum(highlighter_mask) > 0:
        hues = hsv[:,:,0][highlighter_mask]
        sats = hsv[:,:,1][highlighter_mask]
        vals = hsv[:,:,2][highlighter_mask]
        
        print(f"  Pixeles detectados como resaltador: {np.sum(highlighter_mask):,}")
        print(f"\n  Distribucion de HUE (color):")
        
        hist, bins = np.histogram(hues, bins=18, range=(0, 180))
        for i, count in enumerate(hist):
            if count > 100:
                hue_start = i * 10
                hue_end = (i + 1) * 10
                bar = '#' * min(50, count // 1000)
                print(f"    H[{hue_start:3d}-{hue_end:3d}]: {count:8,} {bar}")
        
        print(f"\n  Estadisticas:")
        print(f"    Hue   - min: {np.min(hues):3d}, max: {np.max(hues):3d}, media: {np.mean(hues):.1f}")
        print(f"    Sat   - min: {np.min(sats):3d}, max: {np.max(sats):3d}, media: {np.mean(sats):.1f}")
        print(f"    Value - min: {np.min(vals):3d}, max: {np.max(vals):3d}, media: {np.mean(vals):.1f}")
        
        median_hue = np.median(hues)
        if 15 <= median_hue <= 40:
            print(f"\n  -> Color predominante: AMARILLO (H={median_hue:.0f})")
        elif 40 < median_hue <= 85:
            print(f"\n  -> Color predominante: VERDE (H={median_hue:.0f})")
        elif 85 < median_hue <= 125:
            print(f"\n  -> Color predominante: AZUL/CIAN (H={median_hue:.0f})")
        elif 125 < median_hue <= 145:
            print(f"\n  -> Color predominante: VIOLETA (H={median_hue:.0f})")
        elif median_hue > 145 or median_hue < 15:
            print(f"\n  -> Color predominante: ROSA/ROJO/NARANJA (H={median_hue:.0f})")
        
        unique_hue_ranges = []
        for i, count in enumerate(hist):
            if count > 1000:
                unique_hue_ranges.append((i * 10, (i + 1) * 10))
        
        if len(unique_hue_ranges) > 1:
            print(f"\n  ** Multiples colores detectados en rangos: {unique_hue_ranges}")

def main():
    print("="*60)
    print("ANALISIS DE DISTRIBUCION HSV EN IMAGENES")
    print("="*60)
    
    if os.path.exists(test_images_dir):
        for filename in sorted(os.listdir(test_images_dir)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_path = os.path.join(test_images_dir, filename)
                image_name = filename
                analyze_hsv_distribution(image_path, image_name)
    else:
        print(f"Error: No se encontro el directorio {test_images_dir}")

if __name__ == "__main__":
    main()
