# Barcode/QR code detection in video feed or file using OpenCV and pyzbar
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os

DETECTED_FRAMES_FOLDER = "detected_frames"
os.makedirs(DETECTED_FRAMES_FOLDER, exist_ok=True)

# Define barcode/QR code detection function
def process_frame(frame):
    detected = False
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    #global decoded_text
    # Detect barcodes and QR codes
    decoded_objects = decode(
        blurred_frame, 
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )

    detected_barcodes = []

    for obj in decoded_objects:
        detected = True  # Barcode detected
        
        # Draw bounding box around detected barcode
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Extract barcode details
        decoded_text = obj.data.decode('utf-8')
        barcode_type = obj.type
        detected_barcodes.append({"data": decoded_text, "type": barcode_type})

        # Get Position for overlay text
        x, y, _, _ = obj.rect
        cv2.putText(frame, f"{barcode_type}: {decoded_text}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, detected, detected_barcodes

def process_video(video_path): #Modified to return barcode results
    cap = cv2.VideoCapture(video_path) 
    frame_idx = 0 #For saving frames
    barcode_results = []
    seen_barcodes = set() #For duplication
 
    while cap.isOpened(): #Loop through video frames
        ret, frame = cap.read() 
        if not ret: 
            break

        processed_frame, detected, detected_barcodes = process_frame(frame) 

        if detected:
            for barcode in detected_barcodes:
                barcode_text = barcode["data"]
                if barcode_text not in seen_barcodes:
                    seen_barcodes.add(barcode_text)  # Store unique barcodes
                    barcode_results.append(barcode)  # Save detected barcodes
            
            #Save frames with detected barcodes
            frame_filename = os.path.join(DETECTED_FRAMES_FOLDER, f"detected_{frame_idx:04d}.png")
            cv2.imwrite(frame_filename, processed_frame)

        frame_idx += 1

    cap.release()
    return barcode_results



# video_path = "/Users/Camis/Desktop/test.MOV"  # Change this to your actual test file path
# barcode_data = process_video(video_path)

# if barcode_data:
#     print("Barcodes detected:", barcode_data)
# else:
#     print("No barcodes found in the video.")
