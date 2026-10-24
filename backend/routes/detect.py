from flask import Blueprint, request, jsonify
from utils.yolo_detector import yolo_detect

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
        return jsonify({"mode": "yolo", "model": "ultralytics", "detections": detections})
    except Exception as exc:
        # Avoid returning internal stack traces to the browser.
        return jsonify({
            "error": "YOLO inference failed. Check the backend logs and model weights.",
            "details": str(exc)
        }), 500
