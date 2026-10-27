"""Fine-tune YOLO on a labeled traffic-sign dataset in Ultralytics YOLO format.

Example:
  python scripts/train_traffic_signs.py --data path/to/traffic-signs.yaml --epochs 50
Run training on a GPU/Colab for practical speed. This script does not download a
specific dataset automatically; supply a dataset YAML you have permission to use.
"""
import argparse
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description="Train a traffic-sign YOLO model.")
    parser.add_argument("--data", required=True, help="Dataset YAML containing class names and train/val paths.")
    parser.add_argument("--base-model", default="yolo11n.pt", help="Pretrained model used for transfer learning.")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--project", default="runs/traffic-sign-training")
    parser.add_argument("--name", default="yolo11n-traffic-signs")
    args = parser.parse_args()

    model = YOLO(args.base_model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
        plots=True,
    )
    print("Training finished. Best weights are normally saved under:")
    print(f"{args.project}/{args.name}/weights/best.pt")
    print("Evaluate those weights on a held-out test split before reporting accuracy.")


if __name__ == "__main__":
    main()
