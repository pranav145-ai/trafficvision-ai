"""Traffic-specific YOLO inference for TrafficVision AI.

Default model card:
  https://huggingface.co/subhodeepmoitra/Traffic_signals_detection_YOLOv8m

It includes traffic-light, stop, speed-limit and crosswalk-related classes.
Set TRAFFICVISION_MODEL to a local .pt file to override the default.
"""
import os
from functools import lru_cache
from pathlib import Path

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

    # Downloads once to the Hugging Face cache; later runs reuse the file.
    return hf_hub_download(repo_id=DEFAULT_REPO_ID, filename=DEFAULT_FILENAME)


@lru_cache(maxsize=1)
def load_model():
    return YOLO(default_model_path())


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
            detections.append({
                "class": result.names[class_id],
                "confidence": round(confidence, 4),
                "x": max(0, x1),
                "y": max(0, y1),
                "width": max(0, x2 - x1),
                "height": max(0, y2 - y1)
            })
    return detections
