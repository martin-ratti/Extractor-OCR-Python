import os
import sys
from src.infrastructure.ocr_service import OcrService

def verify_orange_extraction():
    service = OcrService()
    service.DEBUG = True # Enable debug mode to see masks if needed
    
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        print(f"Error: {test_dir} not found.")
        return

    print("=== Verifying Orange Extraction ===")
    
    files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print("No image files found in test_images.")
        return

    for filename in files:
        image_path = os.path.join(test_dir, filename)
        print(f"\nProcessing: {filename}")
        
        # Try specifically with "naranja"
        try:
            text = service.extract_text_from_image(image_path, "naranja")
            print(f"  Result length: {len(text)} chars")
            if "No se encontró texto" in text:
                print("  [FAIL] No text found.")
            elif "Error" in text:
                print(f"  [ERROR] {text}")
            else:
                print(f"  [PASS] Text extracted start: {text[:50]}...")
        except Exception as e:
            print(f"  [EXCEPTION] {e}")

if __name__ == "__main__":
    verify_orange_extraction()
