from pathlib import Path
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Process an image.")
parser.add_argument("image", help="Path to the input image")

args = parser.parse_args()

INPUT_FRAME = Path(args.image)
OUT_DIR = Path("data/processed/debug")
OUT_DIR.mkdir(parents=True, exist_ok=True)

frame = cv2.imread(str(INPUT_FRAME))

if frame is None:
    raise RuntimeError(f"Could not read image: {INPUT_FRAME}")

# OpenCV loads BGR, not RGB
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Start broad: bright + reasonably saturated
# H: 0-179, S: 0-255, V: 0-255
lower = np.array([115, 40, 40])
upper = np.array([165, 255, 255])

mask = cv2.inRange(hsv, lower, upper)

# Clean up noise
kernel = np.ones((3, 3), np.uint8)
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

# Overlay mask on original frame
overlay = frame.copy()
overlay[mask_clean > 0] = [0, 0, 255]  # red overlay in BGR

combined = cv2.addWeighted(frame, 0.5, overlay, 0.5, 0)

# Slight blur to merge nearby pixels
mask_blur = cv2.GaussianBlur(mask_clean, (5, 5), 0)

# Threshold again to re-binarise
_, mask_thresh = cv2.threshold(mask_blur, 127, 255, cv2.THRESH_BINARY)

# Dilate to connect blade segments
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
mask_dilated = cv2.dilate(mask_thresh, kernel, iterations=1)

contours, _ = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contour_img = frame.copy()

for cnt in contours:
    area = cv2.contourArea(cnt)

    # Ignore tiny noise
    if area < 100:
        continue

    rect = cv2.minAreaRect(cnt)
    (cx, cy), (w, h), angle = rect
    
    long_side = max(w, h)
    short_side = min(w, h)

    if long_side < 30:
        continue

    if short_side == 0:
        continue

    aspect_ratio = long_side / short_side

    if aspect_ratio < 2:
        continue
    box = cv2.boxPoints(rect)
    box = box.astype(int)

    cv2.drawContours(contour_img, [box], 0, (0, 255, 0), 2)
    cv2.putText(
        contour_img,
        f"AR {aspect_ratio:.1f}",
        (int(cx), int(cy)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

cv2.imwrite(str(OUT_DIR / "01_original.jpg"), frame)
cv2.imwrite(str(OUT_DIR / "02_mask.jpg"), mask_clean)
cv2.imwrite(str(OUT_DIR / "03_overlay.jpg"), combined)
cv2.imwrite(str(OUT_DIR / "04_mask_dilated.jpg"), mask_dilated)
cv2.imwrite(str(OUT_DIR / "05_contours.jpg"), contour_img)

print(f"Saved debug images to {OUT_DIR}")