import cv2
import os

# Path to video file
video_file = r"C:\barcode-scanner-app\file_example_MOV_1920_2_2MB.mov"
output_folder = r"C:\barcode-scanner-app\extracted_frames"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open video file
cap = cv2.VideoCapture(video_file)

# Check if the video file was successfully opened
if not cap.isOpened():
    print(f"Error: Could not open video file at {video_file}")
else:
    # Get total number of frames
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in the video: {n_frames}")

    frame_idx = 0  # Start index for saving frames
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break  # If no frame is returned, stop processing
        count += 1
        #if count % 10 != 0:
            #continue

        # Save every frame as an image file (every 10 frames)
        frame_filename = os.path.join(output_folder, f"frame_{frame_idx:04d}.png") 
        if frame_idx % 10 == 0:
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(frame_filename, grey)
        ##print(f"Saved: {frame_filename}")

        frame_idx += 1

    # Release video capture when done
    cap.release()
    print("Video processing completed.")
