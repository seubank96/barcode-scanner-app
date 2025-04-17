import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os
import time
from database_website import search_product, add_product, update_quantity, initialize_database  # Import database functions

initialize_database()  # Automatically initialize the database when script runs
recently_scanned = {}  # Store recently scanned barcodes with timestamps
SCAN_RESET_TIME = 5  # Threshold to prevent duplicate scans (in seconds)

# Barcode/QR code detection function for image frames
def process_frame(frame):
    detected = False
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    processed_barcodes = set()
    detected_barcodes = []

    decoded_objects = decode(
        blurred_frame,
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )

    for obj in decoded_objects:
        decoded_text = obj.data.decode('utf-8')

        if decoded_text not in processed_barcodes:
            detected = True
            processed_barcodes.add(decoded_text)
            detected_barcodes.append(decoded_text)

            # Draw bounding box
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            x, y, w, h = obj.rect
            cv2.putText(frame, f"{obj.type}: {decoded_text}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            print(f"Scanned: {decoded_text}")

            current_time = time.time()
            if decoded_text in recently_scanned and (current_time - recently_scanned[decoded_text]) < SCAN_RESET_TIME:
                print(f"Skipping duplicate scan for {decoded_text}")
                continue

            recently_scanned[decoded_text] = current_time

            product = search_product(decoded_text)
            if product:
                update_quantity(decoded_text, 1)
                print(f"Updated inventory for Product ID {decoded_text}")
            else:
                print(f"Product {decoded_text} not found in inventory.")
                category = input("Enter category: ")
                name = input("Enter product name: ")
                price = float(input("Enter price: "))
                quantity = int(input("Enter quantity: "))
                return_period = int(input("Enter return period (days): "))

                add_product(category, decoded_text, name, price, quantity, return_period)
                print(f"Added new product: {name} (ID: {decoded_text})")

    return frame, detected, detected_barcodes

# Function to process uploaded video files
def process_video(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return []

    output_folder = os.path.join(os.getcwd(), "detected_frames")
    os.makedirs(output_folder, exist_ok=True)

    frame_idx = 0
    barcode_detected_count = 0
    detected_barcodes_across_frames = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, detected, detected_barcodes = process_frame(frame)

        for barcode_text in detected_barcodes:
            if barcode_text not in detected_barcodes_across_frames:
                detected_barcodes_across_frames.add(barcode_text)
                barcode_detected_count += 1
                frame_filename = os.path.join(output_folder, f"detected_{frame_idx:04d}.png")
                cv2.imwrite(frame_filename, processed_frame)
                print(f"Saved barcode-detected frame: {frame_filename}")

        frame_idx += 1

    cap.release()
    print(f"Video processing complete. {barcode_detected_count} unique barcodes detected.")
    return list(detected_barcodes_across_frames)