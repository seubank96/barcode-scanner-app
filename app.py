# Main application script
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from Barcode_Scanner_Video_Processing.app_barcode_scanner_video_processing import process_video

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Route to upload a video file
@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file to the upload folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    #process the video
    barcodes = process_video(file_path)
    
    return jsonify({"barcodes":barcodes}), 200

#Run the app
if __name__ == "__main__":
    app.run(debug=True)
