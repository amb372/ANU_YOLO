#!/usr/bin/env python3
import cv2
from ultralytics import YOLO

def main(device="/dev/video0"):
    # 1. Load the pretrained YOLOv8n model
    model = YOLO('yolov8n.pt')

    # 2. Open the USB webcam via V4L2 backend
    cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {device}")

    # 3. Create a resizable window for display
    cv2.namedWindow('YOLOv8 Live', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('YOLOv8 Live', 800, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 4. Run YOLO inference (silent mode)
        results = model(frame, verbose=False)

        # 5. Overlay bounding boxes and labels
        annotated = results[0].plot()

        # 6. Display the annotated frame
        cv2.imshow('YOLOv8 Live', annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()