# TrafficVision AI — Backend

Flask API prototype. The current detection route uses mock results, not a trained YOLO model.

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The server runs at http://localhost:5000. Endpoint: `POST /api/detect`, multipart form field `image`.
