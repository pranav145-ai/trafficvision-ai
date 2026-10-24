# TrafficVision AI

TrafficVision AI is an academic prototype for exploring traffic-sign detection through a React + Vite frontend and a Flask API backend.

## Project status

- The UI starts in demo mode and uses mock detections.
- The Flask endpoint `POST /api/detect` also returns mock detections.
- This repository does **not** include a trained detection model or model weights.
- It is an educational prototype, not a certified road-safety system.

## Structure

- `frontend/` — React and Vite interface
- `backend/` — Flask API and mock detector
- `dataset/` — dataset notes
- `model/weights/` — notes about model weights (weights are not included)

## Run locally

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

See `backend/README.md` and the frontend package scripts for project-specific details.

## Disclaimer

This project is for academic demonstration only. Do not rely on its mock detections for driving, navigation, or any safety-critical decision.
