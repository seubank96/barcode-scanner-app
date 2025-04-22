import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os
import time
from database_website import search_product, add_product, update_quantity, initialize_database  # Import database functions

initialize_database()  # Automatically initialize the database when script runs

# Time threshold to prevent duplicate scans (in seconds)
SCAN_RESET_TIME = 5  
recently_scanned = {}  # Store recently scanned barcodes with timestamps

# Barcode/QR code detection function for image frames 
def process_frame(frame):
    detected = False
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # ✅ Convert to grayscale (Scientific Computing: image preprocessing)
    
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # ✅ Gaussian Blur for noise reduction (Scientific Computing: filtering, convolution)

    processed_barcodes = set()
    detected_barcodes = []

    decoded_objects = decode(
        blurred_frame,
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )  # ✅ Barcode decoding using optimized library (Scientific Computing: signal decoding)

    for obj in decoded_objects:
        decoded_text = obj.data.decode('utf-8')

        if decoded_text not in processed_barcodes:
            detected = True
            processed_barcodes.add(decoded_text)
            detected_barcodes.append(decoded_text)

            # ✅ NumPy for geometric shape construction (Scientific Computing: matrix operations)
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            x, y, w, h = obj.rect
            cv2.putText(frame, f"{obj.type}: {decoded_text}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, detected, detected_barcodes

# Function to process uploaded video files
def process_video(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return []

    output_folder = os.path.join(os.getcwd(), "detected_frames")
    os.makedirs(output_folder, exist_ok=True)  # ✅ File system management (Scientific Computing: file I/O automation)

    frame_idx = 0
    barcode_detected_count = 0
    detected_barcodes_across_frames = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % 2 != 0:
            frame_idx += 1
            continue  # ✅ Frame skipping for performance (Scientific Computing: optimization)

        processed_frame, detected, detected_barcodes = process_frame(frame)

        for barcode_text in detected_barcodes:
            if barcode_text not in detected_barcodes_across_frames:
                detected_barcodes_across_frames.add(barcode_text)

                current_time = time.time()
                if barcode_text in recently_scanned and (current_time - recently_scanned[barcode_text]) < SCAN_RESET_TIME:
                    print(f"Skipping duplicate barcode: {barcode_text}")
                    continue
                recently_scanned[barcode_text] = current_time

                product = search_product(barcode_text)
                if product:
                    update_quantity(barcode_text, 1)
                    print(f"Updated inventory for: {barcode_text}")  # ✅ Conditional logic on data state (Scientific Computing: data-driven decisions)
                else:
                    print(f"Product {barcode_text} not found in database.")
                    category = input("Enter category: ")
                    name = input("Enter product name: ")
                    price = float(input("Enter price: "))  # ✅ Type conversion (Scientific Computing: numerical precision)
                    quantity = int(input("Enter quantity: "))
                    return_period = int(input("Enter return period (days): "))
                    add_product(category, barcode_text, name, price, quantity, return_period)
                    print(f"Added new product: {name} (ID: {barcode_text})")

                # ✅ Save computed output to disk (Scientific Computing: reproducibility and logging)
                barcode_detected_count += 1
                frame_filename = os.path.join(output_folder, f"detected_{frame_idx:04d}.png")
                cv2.imwrite(frame_filename, processed_frame)
                print(f"Saved barcode-detected frame: {frame_filename}")

        frame_idx += 1

    cap.release()
    print(f"Video processing complete. {barcode_detected_count} unique barcodes detected.")  # ✅ Aggregate metric tracking (Scientific Computing: performance monitoring)
    return list(detected_barcodes_across_frames)

