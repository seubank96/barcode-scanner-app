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