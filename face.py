#!/usr/bin/env python3
"""
face_detection.py

Detects faces in an image or video, draws bounding boxes around them,
and saves the annotated output.

Usage:
    # Image:
    python face_detection.py --source path/to/image.jpg --output path/to/out.jpg

    # Video:
    python face_detection.py --source path/to/video.mp4 --output path/to/out.mp4
"""

import cv2
import argparse
import sys

def load_detector():
    # Uses OpenCV's built-in Haar cascade. Adjust path if needed.
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        print(f"Error loading cascade at {cascade_path}", file=sys.stderr)
        sys.exit(1)
    return detector

def process_frame(frame, detector):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True,
                   help='Path to input image or video')
    p.add_argument('--output', required=True,
                   help='Path to save annotated output')
    args = p.parse_args()

    detector = load_detector()

    # Image case
    if args.source.lower().endswith(('.jpg', '.jpeg', '.png')):
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error reading image {args.source}", file=sys.stderr)
            sys.exit(1)
        out = process_frame(img, detector)
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
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        annotated = process_frame(frame, detector)
        writer.write(annotated)

    cap.release()
    writer.release()
    print(f"Annotated video saved to {args.output}")

if __name__ == "__main__":
    main()
