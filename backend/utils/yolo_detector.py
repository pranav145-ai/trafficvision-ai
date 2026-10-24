"""Real YOLO inference for TrafficVision AI.

Default weights are COCO-pretrained YOLOv8n. Set TRAFFICVISION_MODEL to a
custom trained .pt file to detect traffic-sign classes such as speed limits.
"""
import os
from functools import lru_cache
from PIL import Image
from ultralytics import YOLO


@lru_cache(maxsize=1)
def load_model():
    # Ultralytics downloads the default weights on first use if not present.
    model_path = os.getenv("TRAFFICVISION_MODEL", "yolov8n.pt")
    return YOLO(model_path)


def yolo_detect(image_file):
    image_file.stream.seek(0)
    image = Image.open(image_file.stream).convert("RGB")
    model = load_model()
    results = model.predict(source=image, conf=0.25, verbose=False)

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
