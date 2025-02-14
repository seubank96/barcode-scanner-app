# Barcode and QR code scanning module
# Import opencv for computer vision stuff
import cv2
# Import matplotlib so we can visualize an image
from matplotlib import pyplot as plt

import time

# 0 is iPhone camera. 1 is built in webcam
#cap = cv2.VideoCapture(1)

# Get a frame from the capture device
#ret, frame = cap.read()

# If ret = True then we can use that capture device. If ret = False then we cannot use that capture device
#print(ret)

# Shows the capture device
#cv2.imread(frame)

# Stops showing the capture device
#cap.release()

def takePhoto():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    time.sleep(3)
    cv2.imwrite("webcamPhoto.jpg", frame)
    cap.release

cap = cv2.VideoCapture(1)

ret, frame = cap.read()

plt.imshow(frame)

print(cap.isOpened())

while cap.isOpened():
    ret,frame = cap.read()

    # Show image to user
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
