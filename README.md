# TrafficVision AI

TrafficVision AI is an academic prototype with a React + Vite frontend, Flask API, and Ultralytics YOLO inference.

## Detection model

- The backend runs real YOLO inference through `POST /api/detect`.
- Default weights: `yolov8n.pt`, downloaded by Ultralytics on first inference.
- The default COCO model recognizes general object classes including traffic lights, but does **not** reliably recognize speed-limit signs or distinguish red/yellow/green signal states.
- For traffic-sign detection, use a custom model trained on the exact classes you need and set `TRAFFICVISION_MODEL` to its `.pt` file path.

## Run locally (Windows)

Use Python 3.11 or 3.12.

### Backend terminal

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The first model inference downloads the pretrained YOLO weights and needs internet access. The Flask API runs on http://localhost:5000.

### Frontend terminal

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (usually http://localhost:5173), upload an image, and click **Analyze with YOLO**.

## Use custom traffic-sign weights

Place your trained model locally, then set the path before starting Flask:

```powershell
$env:TRAFFICVISION_MODEL="model/weights/your-trained-model.pt"
python app.py
```

Do not commit large model files to Git. The custom model must include the target classes, e.g. speed-limit signs and traffic lights. Traffic-light object detection alone does not classify the signal's illuminated color.

## Structure

- `frontend/` — React and Vite interface
- `backend/` — Flask API and YOLO inference
- `dataset/` — dataset notes
- `model/weights/` — local model weights (not committed)

This is an academic demo, not a safety-critical driving system.
