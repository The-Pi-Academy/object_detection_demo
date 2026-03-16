import os
import sys

import cv2
from ultralytics import YOLO
import supervision as sv

MODEL_BASE_PATH='models/'
MODELS = {
    "DEFAULT": 'yolo26n.pt',
    "YOLO26N": 'yolo26n.pt',
    "YOLO11N": 'yolo11n.pt',
    "YOLO8N": 'yolo8n.pt',

}

def initialize_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    return cap

def load_yolo_model(model_key="DEFAULT"):
    model_file = MODELS[model_key] if model_key in  MODELS else MODELS["DEFAULT"]

    model = os.path.join(MODEL_BASE_PATH, model_file)
    model = YOLO(model)

    return model

def process_frame(frame, model, box_annotator):
    result = model(frame, agnostic_nms=True)[0]
    detections = sv.Detections.from_yolov8(result)
    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, _
        in detections
    ]
    annotated_frame = box_annotator.annotate(
        scene=frame,
        detections=detections,
        labels=labels
    )
    return annotated_frame

def main():
    cap = initialize_camera()

    if len(sys.argv) < 2 or sys.argv[1] not in MODELS:
        model_key = "DEFAULT"
    else:
        model_key = sys.argv[1]
    model = load_yolo_model(model_key)

    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=1
    )

    win_name = f"The Pi Academy Object Detector - {model_key}"
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        annotated_frame = process_frame(frame, model, box_annotator)
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(win_name, annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
