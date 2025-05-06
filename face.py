#!/usr/bin/env python3
"""
face_recognition.py

Detects faces in an image or video, recognizes them against a gallery, 
draws bounding boxes with names, and saves the annotated output.

Usage:
    # Image:
    python face_recognition.py --source path/to/image.jpg \
        --known_dir path/to/known_faces/ \
        --output path/to/out.jpg

    # Video:
    python face_recognition.py --source path/to/video.mp4 \
        --known_dir path/to/known_faces/ \
        --output path/to/out.mp4
"""

import os
import cv2
import argparse
import face_recognition

def load_known_faces(known_dir):
    encodings, names = [], []
    for fname in os.listdir(known_dir):
        path = os.path.join(known_dir, fname)
        name, ext = os.path.splitext(fname)
        if ext.lower() not in ['.jpg', '.jpeg', '.png']:
            continue
        image = face_recognition.load_image_file(path)
        face_locs = face_recognition.face_locations(image)
        if not face_locs:
            continue
        enc = face_recognition.face_encodings(image, known_face_locations=face_locs)[0]
        encodings.append(enc)
        names.append(name)
    return encodings, names

def process_frame(frame, known_encs, known_names):
    rgb = frame[:, :, ::-1]
    locs = face_recognition.face_locations(rgb)
    encs = face_recognition.face_encodings(rgb, locs)
    for (top, right, bottom, left), enc in zip(locs, encs):
        matches = face_recognition.compare_faces(known_encs, enc, tolerance=0.5)
        name = "Unknown"
        if True in matches:
            idx = matches.index(True)
            name = known_names[idx]
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    return frame

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, help='Image or video path')
    p.add_argument('--known_dir', required=True, help='Folder of known faces')
    p.add_argument('--output', required=True, help='Output path')
    args = p.parse_args()

    known_encs, known_names = load_known_faces(args.known_dir)

    # Image?
    if args.source.lower().endswith(('.jpg','.jpeg','.png')):
        img = cv2.imread(args.source)
        out = process_frame(img, known_encs, known_names)
        cv2.imwrite(args.output, out)
        print(f"Saved annotated image to {args.output}")
        return

    # Otherwise assume video
    cap = cv2.VideoCapture(args.source)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vw = cv2.VideoWriter(args.output, fourcc, fps, (w,h))

    while True:
        ret, frame = cap.read()
        if not ret: break
        annotated = process_frame(frame, known_encs, known_names)
        vw.write(annotated)

    cap.release()
    vw.release()
    print(f"Saved annotated video to {args.output}")

if __name__ == '__main__':
    main()
