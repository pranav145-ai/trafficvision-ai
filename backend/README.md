# TrafficVision AI — Backend

Flask API using Ultralytics YOLO inference.

## Default model

The backend downloads and caches the community traffic-related model checkpoint on first inference:
https://huggingface.co/subhodeepmoitra/Traffic_signals_detection_YOLOv8m

Its model card lists traffic-light signal, stop signal, speed-limit signal, crosswalk signal, crosswalk, pedestrian, bus, car and truck classes. It is a YOLOv8m model, so CPU inference can be slower than Nano models. Its reported validation scores come from its publisher and are not TrafficVision AI's own evaluation.

This model was not trained specifically for Indian traffic signs. Check its license and validate on a labeled Indian-road dataset before making accuracy claims.

## Setup (Windows)

Use Python 3.11 or 3.12.

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The first inference needs internet access to download `best.pt` from Hugging Face. It is cached locally for later runs. API: `POST http://localhost:5000/api/detect`, multipart form field `image`.

## Use your own trained model

```powershell
$env:TRAFFICVISION_MODEL="model/weights/best.pt"
python app.py
```

Set the environment variable before starting Flask. The path must point to a local Ultralytics-compatible `.pt` model.

## Evaluate on a labeled dataset

Your dataset must be in Ultralytics YOLO detection format and have a YAML file containing paths and class names for train/val/test.

```powershell
python scripts/evaluate_model.py --data "C:/datasets/traffic-signs/data.yaml" --split test
```

The script reports precision, recall, mAP50 and mAP50-95 where supported, plus plots/confusion matrix and a `metrics.json` report in `runs/evaluation/traffic-sign-test`. Use a held-out test split that was not used to train or tune the model.

## Fine-tune on your own traffic-sign dataset

```powershell
python scripts/train_traffic_signs.py --data "C:/datasets/traffic-signs/data.yaml" --epochs 50
```

For faster training, use a compatible GPU or Google Colab. Training requires correctly labeled images and YOLO-format bounding-box annotations. Set `TRAFFICVISION_MODEL` to the resulting `best.pt` to use the fine-tuned model.

## Metrics to report

- Precision: proportion of predicted detections that are correct.
- Recall: proportion of labeled objects that were detected.
- mAP@0.50: mean average precision at IoU threshold 0.50.
- mAP@0.50:0.95: mean AP averaged over IoU thresholds 0.50 through 0.95.
- Inference time: measure on the target laptop and report the device and image size.

Do not claim an accuracy result until you have run the evaluation script on a labeled held-out test set. This is an academic prototype, not a safety-critical system.
