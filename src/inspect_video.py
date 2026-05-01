from pathlib import Path
import cv2

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = PROJECT_ROOT / "data" / "cuts" / "fight_01.mp4"
OUT_DIR = PROJECT_ROOT / "data" / "processed" / "frames"
OUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = frame_count / fps if fps else 0

print(f"Video: {VIDEO_PATH}")
print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")
print(f"Frames: {frame_count}")
print(f"Duration: {duration:.2f} seconds")

for second in range(int(duration)):
    frame_index = int(second * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    ok, frame = cap.read()
    if not ok:
        print(f"Skipped frame {frame_index}")
        continue

    out_path = OUT_DIR / f"fight_001_t{second:03d}.jpg"
    cv2.imwrite(str(out_path), frame)

cap.release()

print(f"Saved sample frames to: {OUT_DIR}")    