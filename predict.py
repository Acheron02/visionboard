import cv2
import os
import numpy as np
from ultralytics import YOLO

# Load YOLO model once
MODEL_PATH = "defect_8.pt"
model = YOLO(MODEL_PATH)

# Mapping from YOLO class → (short label, full description)
CLASS_MAP = {
    "open": ("A", "Broken Traces"),
    "short": ("B", "Short Circuits"),
    "90-degree": ("C", "90 Degree Angle"),
}

# Colors for each class (BGR format for OpenCV)
COLOR_MAP = {
    "A": (0, 0, 255),     # Red for Broken Traces
    "B": (0, 255, 0),     # Green for Short Circuits
    "C": (255, 0, 0),     # Blue for 90 Degree Angle
}


def draw_annotations(image, result, show_confidence=False):
    """
    Draw incremental letter+number annotations (A1, A2, B1, …),
    auto-adjusted outside bounding boxes.
    """
    detections = []
    ih, iw = image.shape[:2]

    # Counter for each class (A, B, C …)
    class_counters = {k: 0 for k, _ in CLASS_MAP.values()}

    if result.boxes is None:
        return image, detections

    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = result.names[cls_id]

        # Normalize label to match CLASS_MAP keys
        norm_label = label.strip().lower()

        # Map to letter + full description
        short_label, full_label = CLASS_MAP.get(norm_label, ("?", label))

        # Increment class counter
        class_counters[short_label] += 1
        numbered_label = f"{short_label}{class_counters[short_label]}"

        # Pick color (default yellow if not found)
        color = COLOR_MAP.get(short_label, (0, 255, 255))

        # Coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(iw - 1, x2), min(ih - 1, y2)

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Prepare font + text size
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_label = numbered_label
        if show_confidence:
            text_label += f" ({conf*100:.1f}%)"

        text_size, _ = cv2.getTextSize(text_label, font, 1.0, 2)
        text_w, text_h = text_size

        # Try placing above; if not enough space, place below
        if y1 - text_h - 5 >= 0:
            text_x = x1
            text_y = y1 - 5
        else:
            text_x = x1
            text_y = y2 + text_h + 5

        # Draw the label
        cv2.putText(
            image,
            text_label,
            (text_x, text_y),
            font,
            1.0,
            color,
            2,
            cv2.LINE_AA,
        )

        # Save detection for summary
        detections.append({
            "id": numbered_label,
            "class": full_label,
            "confidence": round(conf, 2),
            "bbox": [x1, y1, x2, y2],
        })

    return image, detections


def analyze_image(image_path: str, save_dir: str = "processed_results", show_confidence=False):
    """
    Run YOLO prediction on a single image and save annotated result.
    Returns the path to the annotated image and a summary dictionary.
    """
    os.makedirs(save_dir, exist_ok=True)

    results = model.predict(image_path, conf=0.3, imgsz=320, verbose=False)
    if not results:
        raise ValueError("No results returned by YOLO.")

    result = results[0]

    # Load original image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load {image_path}")

    # Draw custom annotations (letters+index or with confidence if enabled)
    annotated, detections = draw_annotations(img, result, show_confidence=show_confidence)

    # Save processed image
    filename = os.path.basename(image_path)
    processed_path = os.path.join(save_dir, f"processed_{filename}")
    success = cv2.imwrite(processed_path, annotated)
    if not success:
        raise IOError(f"Failed to save processed image at {processed_path}")

    # Build summary (full text descriptions)
    summary = {
        "file": image_path,
        "processed_file": processed_path,
        "detections": detections,
    }

    return processed_path, summary
