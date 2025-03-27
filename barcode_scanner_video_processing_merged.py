# Barcode/QR code detection in video feed or file using OpenCV and pyzbar
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os

# Define barcode/QR code detection function
def process_frame(frame):
    detected = False
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    global decoded_text
    # Detect barcodes and QR codes
    decoded_objects = decode(
        blurred_frame, 
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )

    for obj in decoded_objects:
        detected = True  # Barcode detected
        
        # Draw bounding box around detected barcode
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Draw decoded text above the barcode
        decoded_text = obj.data.decode('utf-8')
        x, y, w, h = obj.rect
        cv2.putText(frame, f"{obj.type}: {decoded_text}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Decoded {obj.type}: {decoded_text}")


    return frame, detected

# Ask user to select source
choice = input("Enter '0' for camera feed or '1' for video file: ")

# Initialize the video source
if choice == '0':
    cap = cv2.VideoCapture(0)  # Use the default camera
# elif choice == '1':
    # video_file = r"C:\Projects\barcode-scanner-app\file_example_MOV_1920_2_2MB.mov"
    # cap = cv2.VideoCapture(video_file)
else:
    print("Invalid input. Exiting the program.")
    exit()

# Set up output folder
output_folder = r"C:\Projects\barcode-scanner-app\detected_frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check if the video/camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera or video file.")
else:
    frame_idx = 0  # Frame index for saving
    barcode_detected_count = 0

    detected_barcodes = []  # List to store detected barcode data

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video or camera feed interrupted

        # Process frame for barcode detection
        processed_frame, detected = process_frame(frame)

        # Save frames with detected barcodes
        if detected and decoded_text not in detected_barcodes:
            detected_barcodes.append(decoded_text)
            barcode_detected_count += 1
            frame_filename = os.path.join(output_folder, f"detected_{frame_idx:04d}.png")
            cv2.imwrite(frame_filename, processed_frame)
            print(f"Saved barcode-detected frame: {frame_filename}")

        # Display the frame (for camera feed)
        if choice == '0':
            cv2.imshow('Live Barcode Scanner', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frame_idx += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print(f"Processing completed. Total barcode-detected frames: {barcode_detected_count, decoded_text}")