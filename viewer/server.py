from pathlib import Path
from flask import Flask, jsonify, send_from_directory

REPO_ROOT = Path(__file__).resolve().parents[1]
DEBUG_DIR = REPO_ROOT / "data" / "processed" / "debug"
VIEWER_DIR = REPO_ROOT / "viewer"

app = Flask(__name__, static_folder=str(VIEWER_DIR), static_url_path="")

@app.route("/")
def index():
    return send_from_directory(VIEWER_DIR, "index.html")

@app.route("/style.css")
def style():
    return send_from_directory(VIEWER_DIR, "style.css")

@app.route("/api/images")
def list_images():
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    images = sorted(
        p.name for p in DEBUG_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in exts
    )
    return jsonify(images)

@app.route("/debug/<path:filename>")
def debug_image(filename):
    return send_from_directory(DEBUG_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True, port=8000)