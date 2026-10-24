def mock_detect(image_file):
    # Educational placeholder; this is NOT real YOLO inference.
    return [{
        "class": "Stop Sign",
        "confidence": 0.964,
        "x": 120,
        "y": 85,
        "width": 80,
        "height": 95
    }]
