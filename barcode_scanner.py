# Barcode and QR code scanning module
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

def select_camera():
    
    while True:
        try:
            cam_source = int(input("Enter 0 for default camera or 1 for external camera: "))
            if cam_source in [0, 1]:
                return cam_source
            else:
                print("Invalid input. Please enter 0 or 1.") # shows error message if user enters a value other than 0 or 1
        except ValueError:
            print("Invalid input. Please enter an integer (0 or 1).") # shows error message if user enters a non-integer value

def process_frame(frame):
    """
    Processes a video frame to detect and decode barcodes/QR codes.
    Args:
        frame (numpy.ndarray): The video frame to process.
    Returns:
        numpy.ndarray: The annotated frame with detected barcodes/QR codes.
    """
    # Convert frame to grayscale for better decoding (removes color to simplify processing)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0) # 5x5 pixel grid for blurring
    
    # Decode barcodes and QR codes
    decoded_objects = decode(blurred_frame, symbols= [ZBarSymbol.QRCODE, ZBarSymbol.EAN13, ZBarSymbol.UPCA, ZBarSymbol.CODE128])
    
    # Read the video stream
    success, img = cap.read()
    #print(success)

    if not success:
        break
  
    for code in decode(img):
        #print(code)

        decoded_data = code.data.decode("utf-8")

        rect_pts = code.rect

        if decoded_data:
            pts = np.array(code.polygon)
            cv2.polylines(img, [pts], True, (0, 255, 0), 3)
            cv2.putText(img, str(decoded_data), (rect_pts[0], rect_pts[1]), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)


    cv2.imshow("Video Stream", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()