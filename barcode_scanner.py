import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import os
import time
from database import search_product, add_product, update_quantity, initialize_database  # Import database functions

# Automatically initialize the database when script runs
initialize_database()

# Dictionary to store recently scanned barcodes with timestamps
recently_scanned = {}

# Time threshold to prevent duplicate scans (in seconds)
SCAN_RESET_TIME = 5  # You can adjust this

# Define barcode/QR code detection function
def process_frame(frame):
    detected = False
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    processed_barcodes = set()  # Track processed barcodes in this frame
    detected_barcodes = []  # List to return detected barcodes

    # Detect barcodes and QR codes
    decoded_objects = decode(
        blurred_frame, 
        symbols=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128]
    )

    for obj in decoded_objects:
        decoded_text = obj.data.decode('utf-8') # Decode barcode data

        # Ensure barcode is processed only once per frame
        if decoded_text not in processed_barcodes:
            detected = True
            processed_barcodes.add(decoded_text)  
            detected_barcodes.append(decoded_text)  

            # Draw bounding box
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display text above barcode
            x, y, w, h = obj.rect
            cv2.putText(frame, f"{obj.type}: {decoded_text}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            print(f"Scanned: {decoded_text}")

            # Prevent duplicate updates within the reset time
            current_time = time.time() # Get current time
            if decoded_text in recently_scanned and (current_time - recently_scanned[decoded_text]) < SCAN_RESET_TIME: # Check if barcode was recently scanned
                print(f"Skipping duplicate scan for {decoded_text}")
                continue  

            recently_scanned[decoded_text] = current_time  # Update the scanned barcode with current time

            # Check if the barcode exists in the database
            product = search_product(decoded_text)

            if product:
                update_quantity(decoded_text, 1)  # Increment quantity by 1
                print(f"Updated inventory for Product ID {decoded_text}")

            else: # If product not found, add new product to the database
                print(f"Product {decoded_text} not found in inventory.")
                category = input("Enter category: ")
                name = input("Enter product name: ")
                price = float(input("Enter price: "))
                quantity = int(input("Enter quantity: "))
                return_period = int(input("Enter return period (days): "))

                add_product(category, decoded_text, name, price, quantity, return_period) # Add new product
                print(f"Added new product: {name} (ID: {decoded_text})")

    return frame, detected, detected_barcodes  

# Ask user to select source
choice = input("Enter '0' for camera feed or '1' for video file: ")

# Initialize the video source
if choice == '0':
    cap = cv2.VideoCapture(0)  
else:
    print("Invalid input. Exiting the program.")
    exit()

# Set up output folder for saving detected frames
output_folder = r"C:\Projects\barcode-scanner-app\detected_frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check if the video/camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera or video file.")
else:
    frame_idx = 0  
    barcode_detected_count = 0

    detected_barcodes_across_frames = set()  

    while cap.isOpened(): # Loop through video frames
        ret, frame = cap.read()
        if not ret:
            break  

        processed_frame, detected, detected_barcodes = process_frame(frame) # Process the frame

        for barcode_text in detected_barcodes: # Save detected barcodes to a set
            if barcode_text not in detected_barcodes_across_frames:
                detected_barcodes_across_frames.add(barcode_text) # Add new barcode to the set
                barcode_detected_count += 1
                frame_filename = os.path.join(output_folder, f"detected_{frame_idx:04d}.png") # Save the frame
                cv2.imwrite(frame_filename, processed_frame)
                print(f"Saved barcode-detected frame: {frame_filename}")

        if choice == '0':
            cv2.imshow('Live Barcode Scanner', processed_frame) # Display the frame

            key = cv2.waitKey(1) & 0xFF # Wait for key press
            if key == ord('q'):  # Press 'q' to quit
                break  
            if key == ord('r'):   # Press 'r' to reset the scan
                recently_scanned.clear()  
                print("Scan reset! You can now scan the same barcode again.")

        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processing completed. Total barcode-detected frames: {barcode_detected_count}")

# End of the script