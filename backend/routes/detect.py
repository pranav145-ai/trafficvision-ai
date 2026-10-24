from flask import Blueprint, request, jsonify
from utils.mock_detector import mock_detect

detect_bp = Blueprint("detect", __name__)
ALLOWED = {"image/jpeg", "image/png", "image/webp"}

@detect_bp.post("/detect")
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image field was provided."}), 400
    image = request.files["image"]
    if image.mimetype not in ALLOWED:
        return jsonify({"error": "Unsupported image type."}), 400
    # Replace mock_detect() with a real inference function when model weights exist.
    return jsonify({"mode": "mock", "detections": mock_detect(image)})
