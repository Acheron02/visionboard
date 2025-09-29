import cv2
import os
from ultralytics import YOLO

# Load YOLO model once
MODEL_PATH = "defect_7.pt"
model = YOLO(MODEL_PATH)

def analyze_image(image_path: str, save_dir: str = "processed_results"):
    """
    Run YOLO prediction on a single image and save annotated result.
    Returns the path to the annotated image and a summary dictionary.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Run YOLO
    results = model.predict(image_path, conf=0.5, imgsz=320, verbose=False)

    if not results:
        raise ValueError("No results returned by YOLO.")

    result = results[0]

    # Annotate
    annotated = result.plot()

    # Save processed image
    filename = os.path.basename(image_path)
    processed_path = os.path.join(save_dir, f"processed_{filename}")
    cv2.imwrite(processed_path, annotated)

    # Build report (simple summary)
    detections = []
    if result.boxes is not None:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            detections.append({
                "class": result.names[cls],
                "confidence": round(conf, 2)
            })

    summary = {
        "file": image_path,
        "processed_file": processed_path,
        "detections": detections
    }

    return processed_path, summary
