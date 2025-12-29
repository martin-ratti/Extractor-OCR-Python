import cv2
import numpy as np
import os

test_images_dir = "test_images"
with open("hue_summary.txt", "w") as out:
    for f in sorted(os.listdir(test_images_dir)):
        if f.endswith('.jpg'):
            image = cv2.imread(os.path.join(test_images_dir, f))
            if image is None: continue
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Broader mask for highlighter detection
            mask = (hsv[:,:,1] > 50) & (hsv[:,:,2] > 100)
            if np.sum(mask) > 100:
                hues = hsv[:,:,0][mask]
                hist, _ = np.histogram(hues, bins=18, range=(0, 180))
                max_bin = np.argmax(hist)
                out.write(f"{f}: Median={np.median(hues):.1f}, MaxBin={max_bin*10}-{(max_bin+1)*10}\n")
                # write histogram as a simple list string
                out.write(f"Hist: {list(hist)}\n")
