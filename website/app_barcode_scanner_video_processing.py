import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os

# Get absolute path for the detected frames folder
DETECTED_FRAMES_FOLDER = os.path.abspath("detected_frames")
os.makedirs(DETECTED_FRAMES_FOLDER, exist_ok=True)
print(f"Saving frames to: {DETECTED_FRAMES_FOLDER}")  # Debug print

def process_frame(frame):
    detected_barcodes = []
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    decoded_objects = decode(
        blurred_frame, 
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )

    for obj in decoded_objects:
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        decoded_text = obj.data.decode('utf-8')
        barcode_type = obj.type
        detected_barcodes.append({"data": decoded_text, "type": barcode_type})

        x, y, _, _ = obj.rect
        cv2.putText(frame, f"{barcode_type}: {decoded_text}", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame, len(detected_barcodes) > 0, detected_barcodes

def process_video(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open video file")
    
    unique_barcodes = set()
    barcode_results = []

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, detected, frame_barcodes = process_frame(frame)
        frame_count += 1

        if detected:
            for barcode in frame_barcodes:
                barcode_id = f"{barcode['type']}_{barcode['data']}"
                
                if barcode_id not in unique_barcodes:
                    unique_barcodes.add(barcode_id)
                    barcode_results.append(barcode)
                    
                    # Generate safe filename
                    safe_data = "".join(c for c in barcode['data'] if c.isalnum() or c in ('-', '_'))
                    filename = f"{barcode['type']}_{safe_data}.png"
                    filepath = os.path.join(DETECTED_FRAMES_FOLDER, filename)
                    
                    print(f"Saving {filename}")  # Debug print
                    try:
                        cv2.imwrite(filepath, processed_frame)
                        if not os.path.exists(filepath):
                            print(f"Warning: File {filename} not saved successfully!")
                    except Exception as e:
                        print(f"Error saving {filename}: {str(e)}")

    cap.release()
    print(f"Processing complete. Found {len(barcode_results)} unique barcodes.")
    return barcode_results