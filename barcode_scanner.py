<<<<<<< HEAD
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
    
    for obj in decoded_objects:
        # Extract the bounding box coordinates
        points = obj.polygon # Get the polygon points of the barcode/QR code
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32) # Reshape the points array to a NumPy array
            pts = pts.reshape((-1, 1, 2)) # Reshape the points array to a 3D array
            # Draw the bounding box
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        
        # Extract and draw the decoded text
        decoded_text = obj.data.decode('utf-8') # Decode the data byte string to a UTF-8 string
        x, y, w, h = obj.rect
        # Draw the text
        cv2.putText(frame, decoded_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Decoded {obj.type}: {decoded_text}")

    return frame

def main():
    # Select the camera source
    cam_source = select_camera()
    
    # Initialize the video capture object
    cap = cv2.VideoCapture(cam_source)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Press 'q' to quit.")
    
    try: # Try block to handle exceptions
        while True:

            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            # Process the frame
            processed_frame = process_frame(frame)
            
            # Display the resulting frame
            cv2.imshow('Barcode/QR Code Scanner', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Release the capture and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__": # Check if the script is being run directly
    main()
=======
# import libraries
from pyzbar.pyzbar import decode
import cv2
import numpy as np

# The following code reads a QR code from a video stream

# Initialize running as True
running = True

# Run while true
while True:

    # Try this block
    try:

        camSource = int(input("Enter 0 to use iPhone Camera or 1 to use MacBook Camera: "))
        if camSource == 0 or camSource == 1:
            break  # Exit the loop if the input is valid
        else:
            print("Incorrect Input. Please enter 0 or 1.")

    # Catch the error
    except ValueError:
        print("Invalid input. Please enter an integer (0 or 1).")


if camSource == 1:
    cap = cv2.VideoCapture(1)
else:
    cap = cv2.VideoCapture(0)

# Loop while running is True
while running:
    
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
>>>>>>> cee65ff297f350e9954c0de8f7119c0bcf5044eb
