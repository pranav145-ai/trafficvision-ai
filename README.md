# TrafficVision AI

TrafficVision AI is a React + Vite frontend with a Flask API and a traffic-specific Ultralytics YOLO detector.

## Model

The backend defaults to a community YOLOv8m model hosted on Hugging Face:
https://huggingface.co/subhodeepmoitra/Traffic_signals_detection_YOLOv8m

The publisher lists classes for traffic-light signals, stop signals, speed-limit signals, crosswalk-related objects, pedestrians, buses, cars and trucks. The model downloads automatically on first inference and is cached locally. Its reported validation metrics are from the publisher, not our own tests. It is not specifically trained for Indian road signs, so evaluate it on suitable local data before claiming accuracy.

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

The first inference requires internet access to download model weights from Hugging Face. Flask runs on http://localhost:5000.

### Frontend terminal

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL (usually http://localhost:5173), upload an image, and click **Analyze with YOLO**.

## Evaluate model performance

Use a labeled dataset in Ultralytics YOLO format with a dataset YAML file containing train/val/test paths and class names:

```powershell
cd backend
python scripts/evaluate_model.py --data "C:/datasets/traffic-signs/data.yaml" --split test
```

Metrics and plots are saved under `backend/runs/evaluation/traffic-sign-test`. Use a held-out test split that was not used for training or tuning. Report precision, recall, mAP@0.50, mAP@0.50:0.95 and inference time; don't invent results.

## Fine-tune a model

```powershell
cd backend
python scripts/train_traffic_signs.py --data "C:/datasets/traffic-signs/data.yaml" --epochs 50
```

Use a compatible GPU or Google Colab for faster training. The dataset must have labeled bounding boxes and YOLO-format annotations. To use local weights:

```powershell
$env:TRAFFICVISION_MODEL="model/weights/best.pt"
python app.py
```

## Structure

- `frontend/` — React and Vite interface
- `backend/` — Flask API, YOLO inference, training and evaluation scripts
- `backend/scripts/` — training and evaluation utilities
- `dataset/` — dataset notes

Academic prototype only; not for safety-critical driving decisions.
