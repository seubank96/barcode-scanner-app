# Main application script
from flask import Flask
import os


print("helloWorld!")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DETECTED_FRAMES_FOLDER = "detected_frames"


# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTED_FRAMES_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#@app.route("/upload", methods=["POST"])
