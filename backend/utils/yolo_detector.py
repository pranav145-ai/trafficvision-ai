"""Traffic-specific YOLO inference and traffic-light color estimation."""
import os
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from huggingface_hub import hf_hub_download
from PIL import Image
from ultralytics import YOLO

DEFAULT_REPO_ID = "subhodeepmoitra/Traffic_signals_detection_YOLOv8m"
DEFAULT_FILENAME = "best.pt"


@lru_cache(maxsize=1)
def default_model_path():
    local_path = os.getenv("TRAFFICVISION_MODEL")
    if local_path:
        path = Path(local_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(
                f"TRAFFICVISION_MODEL points to a missing file: {path}"
            )
        return str(path.resolve())
    return hf_hub_download(repo_id=DEFAULT_REPO_ID, filename=DEFAULT_FILENAME)


@lru_cache(maxsize=1)
def load_model():
    return YOLO(default_model_path())


def estimate_signal_color(image, box):
    """Estimate illuminated red/amber/green pixels inside a traffic-light box.

    This is a color heuristic, not a trained signal-state classifier. It may
    return UNKNOWN when the crop is small, dark, or has no clear signal color.
    """
    x1, y1, x2, y2 = box
    crop = image.crop((max(0, x1), max(0, y1), min(image.width, x2), min(image.height, y2)))
    if crop.width < 4 or crop.height < 4:
        return {"signal_color": "UNKNOWN", "signal_color_confidence": 0.0,
                "signal_color_method": "HSV color heuristic"}

    hsv = cv2.cvtColor(np.array(crop.convert("RGB")), cv2.COLOR_RGB2HSV)
    hue, saturation, value = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    bright = (saturation >= 90) & (value >= 130)

    masks = {
        "RED": bright & ((hue <= 10) | (hue >= 170)),
        "AMBER": bright & (hue >= 12) & (hue <= 35),
        "GREEN": bright & (hue >= 36) & (hue <= 90),
    }
    counts = {name: int(mask.sum()) for name, mask in masks.items()}
    total = sum(counts.values())
    if total < 3:
        return {"signal_color": "UNKNOWN", "signal_color_confidence": 0.0,
                "signal_color_method": "HSV color heuristic"}

    color = max(counts, key=counts.get)
    share = counts[color] / total
    if counts[color] < 3 or share < 0.45:
        color = "UNKNOWN"
    return {
        "signal_color": color,
        "signal_color_confidence": round(share if color != "UNKNOWN" else 0.0, 3),
        "signal_color_method": "HSV color heuristic",
    }


def yolo_detect(image_file):
    image_file.stream.seek(0)
    image = Image.open(image_file.stream).convert("RGB")
    model = load_model()
    results = model.predict(source=image, conf=0.25, imgsz=640, verbose=False)

    detections = []
    for result in results:
        if result.boxes is None:
            continue
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
            detection = {
                "class": result.names[class_id],
                "confidence": round(confidence, 4),
                "x": max(0, x1),
                "y": max(0, y1),
                "width": max(0, x2 - x1),
                "height": max(0, y2 - y1),
            }
            class_name = str(result.names[class_id]).lower().replace("_", " ").replace("-", " ")
            if "traffic" in class_name and ("light" in class_name or "signal" in class_name):
                detection.update(estimate_signal_color(image, (x1, y1, x2, y2)))
            detections.append(detection)
    return detections
