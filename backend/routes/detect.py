from flask import Blueprint, request, jsonify
from utils.yolo_detector import yolo_detect, DEFAULT_REPO_ID

detect_bp = Blueprint("detect", __name__)
ALLOWED = {"image/jpeg", "image/png", "image/webp"}

@detect_bp.post("/detect")
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image field was provided."}), 400
    image = request.files["image"]
    if image.mimetype not in ALLOWED:
        return jsonify({"error": "Unsupported image type."}), 400
    try:
        detections = yolo_detect(image)
        return jsonify({
            "mode": "yolo",
            "model": "Traffic-specific YOLOv8m",
            "model_source": DEFAULT_REPO_ID,
            "detections": detections
        })
    except Exception as exc:
        # Include a concise message for troubleshooting; detailed traces stay in backend logs.
        return jsonify({
            "error": "YOLO inference failed. Check internet access for the first model download and inspect the backend terminal.",
            "details": str(exc)
        }), 500
