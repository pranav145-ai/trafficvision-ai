# TrafficVision AI — Backend

Flask API using Ultralytics YOLO inference for uploaded images.

## Setup (Windows)

Use Python 3.11 or 3.12 for the smoothest compatibility with PyTorch/Ultralytics.

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The first inference downloads the default `yolov8n.pt` weights if they are not cached. This may take time and requires internet access. Later runs can use the cached weights.

API: `POST http://localhost:5000/api/detect`, multipart form field `image`.

## Important model limitation

The default `yolov8n.pt` is pretrained on COCO. It can detect general objects including **traffic lights**, but it is not a traffic-sign model and does not reliably recognize speed-limit signs or distinguish red/yellow/green signal states. For those features, supply a traffic-sign/traffic-light model trained on the required classes:

```powershell
$env:TRAFFICVISION_MODEL="model/weights/your-trained-model.pt"
python app.py
```

The custom model's class names are returned by YOLO. Keep model weights out of Git if the file is large; place them locally at the configured path. This is an academic demo, not a safety-critical system.
