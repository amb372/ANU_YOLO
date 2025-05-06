#!/usr/bin/env python3
"""
yolo_object_detection.py

Runs YOLOv8 detection on an image or video, draws bounding boxes with class names
and confidences, and saves the annotated output.

Usage:
    # Image:
    python yolo_object_detection.py --source path/to/image.jpg \
        --model yolov8n.pt --output path/to/out.jpg

    # Video:
    python yolo_object_detection.py --source path/to/video.mp4 \
        --model yolov8n.pt --output path/to/out.mp4
"""

import argparse
import cv2
from ultralytics import YOLO

def draw_boxes(frame, result, class_names):
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls  = int(box.cls[0])
        label = f"{class_names[cls]} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    return frame

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, help='Image or video path')
    p.add_argument('--model',  required=True, help='Path to YOLOv8 .pt weights')
    p.add_argument('--output', required=True, help='Output path')
    args = p.parse_args()

    model = YOLO(args.model)
    names = model.names

    # Image?
    if args.source.lower().endswith(('.jpg', '.jpeg', '.png')):
        results = model(args.source)[0]
        img = cv2.imread(args.source)
        out = draw_boxes(img, results, names)
        cv2.imwrite(args.output, out)
        print(f"Annotated image saved to {args.output}")
        return

    # Video
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"Error opening video {args.source}", file=sys.stderr)
        sys.exit(1)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps    = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(args.output, fourcc, fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)[0]
        annotated = draw_boxes(frame, results, names)
        writer.write(annotated)

    cap.release()
    writer.release()
    print(f"Annotated video saved to {args.output}")

if __name__ == "__main__":
    main()
