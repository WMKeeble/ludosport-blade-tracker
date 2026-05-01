from pathlib import Path
import cv2
import numpy as np

INPUT_FRAME = Path("data/processed/frames/fight_001_t001.jpg")
OUT_DIR = Path("data/processed/debug_masks")
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

combined = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

cv2.imwrite(str(OUT_DIR / "original.jpg"), frame)
cv2.imwrite(str(OUT_DIR / "mask.jpg"), mask_clean)
cv2.imwrite(str(OUT_DIR / "overlay.jpg"), combined)

print(f"Saved debug images to {OUT_DIR}")