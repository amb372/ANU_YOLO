#!/usr/bin/env python3
"""
face_detection_yolo.py

Detects faces in an image or video using a YOLOv8 model,
applies a confidence threshold and NMS, draws bounding boxes,
and saves the annotated output.

Usage:
    # Image:
    python face_detection_yolo.py --source path/to/image.jpg --output path/to/out.jpg

    # Video:
    python face_detection_yolo.py --source path/to/video.mp4 --output path/to/out.mp4
"""

import cv2
import argparse
import sys
import os
from ultralytics import YOLO

# ──────────────────────────────────────────────────────────────────────────────
# Globals you can tune:
MODEL_PATH          = 'yolov8n-face-lindevs.pt'  # your face-trained YOLOv8 weights
CONFIDENCE_THRESHOLD = 0.5               # minimum confidence to keep a detection
NMS_THRESHOLD        = 0.3               # IoU threshold for non-max suppression
# ──────────────────────────────────────────────────────────────────────────────

def load_model():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file {MODEL_PATH} not found", file=sys.stderr)
        sys.exit(1)
    try:
        model = YOLO(MODEL_PATH)
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}", file=sys.stderr)
        sys.exit(1)

def process_frame(frame, model):
    try:
        # Run inference (returns list of Results)
        results = model(frame, conf=CONFIDENCE_THRESHOLD, iou=NMS_THRESHOLD)[0]
        # results.boxes: xyxy + confidence + class
        for box in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = box
            # draw only "face" class (cls==0 if your model is single-class)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
            cv2.putText(frame, f"{conf:.2f}", (int(x1), int(y1)-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        return frame
    except Exception as e:
        print(f"Error processing frame: {str(e)}", file=sys.stderr)
        return frame

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, help='Path to input image or video')
    p.add_argument('--output', required=True, help='Path to save annotated output')
    args = p.parse_args()

    # Check if source file exists
    if not os.path.exists(args.source):
        print(f"Error: Source file {args.source} not found", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model = load_model()
    cap = None
    writer = None

    try:
        # Image case
        if args.source.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = cv2.imread(args.source)
            if img is None:
                print(f"Error reading image {args.source}", file=sys.stderr)
                sys.exit(1)
            out = process_frame(img, model)
            cv2.imwrite(args.output, out)
            print(f"Annotated image saved to {args.output}")
            return

        # Video case
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
            if not ret: break
            annotated = process_frame(frame, model)
            writer.write(annotated)

        print(f"Annotated video saved to {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        if cap is not None:
            cap.release()
        if writer is not None:
            writer.release()

if __name__ == "__main__":
    main()
