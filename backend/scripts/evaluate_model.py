"""Evaluate a YOLO detector on a labeled test/validation split.

Example:
  python scripts/evaluate_model.py --data path/to/data.yaml --split test
"""
import argparse
import json
from pathlib import Path

from ultralytics import YOLO
from utils.yolo_detector import default_model_path


def main():
    parser = argparse.ArgumentParser(description="Evaluate a YOLO traffic-sign model.")
    parser.add_argument("--data", required=True, help="Dataset YAML with train/val/test splits.")
    parser.add_argument("--split", choices=["val", "test"], default="test")
    parser.add_argument("--model", default=None, help="Local .pt path; defaults to the traffic-sign model.")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.001, help="Low confidence threshold for mAP evaluation.")
    parser.add_argument("--project", default="runs/evaluation")
    parser.add_argument("--name", default="traffic-sign-test")
    args = parser.parse_args()

    weights = args.model or default_model_path()
    model = YOLO(weights)
    metrics = model.val(
        data=args.data,
        split=args.split,
        imgsz=args.imgsz,
        conf=args.conf,
        plots=True,
        project=args.project,
        name=args.name,
        exist_ok=True,
    )

    summary = {key: float(value) for key, value in metrics.results_dict.items()}
    output_dir = Path(args.project) / args.name
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "metrics.json"
    report_path.write_text(json.dumps({
        "model": str(weights),
        "dataset_yaml": args.data,
        "split": args.split,
        "image_size": args.imgsz,
        "confidence_threshold": args.conf,
        "metrics": summary,
    }, indent=2), encoding="utf-8")

    print("\nEvaluation summary")
    for key, value in summary.items():
        print(f"{key}: {value:.4f}")
    print(f"\nFull metrics JSON: {report_path.resolve()}")
    print(f"Plots and confusion matrix: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
