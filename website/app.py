# Main application script

from flask import *
from werkzeug.utils import secure_filename
import os
from barcode_scanner import process_video

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

'''@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route("/home.html")
def home():
    return render_template('home.html')  # Render the HTML form'''

# === FLASK ROUTE FOR WEB UPLOAD ===
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

@app.route('/')
def index():
    return render_template('index.html')
'''
    <h1>Barcode Scanner Test</h1>
    <form method=post enctype=multipart/form-data action="/upload">
      <input type=file name=video accept="video/*">
      <input type=submit value="Upload Video">
    </form>
    '''

#Run the app
if __name__ == "__main__":
    app.run(debug=True)
