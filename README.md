# Barcode Scanner Application

## Project Overview
This application processes video files to extract barcode and QR code data, then updates an inventory system automatically. The goal is to improve warehouse and inventory management efficiency by automating the scanning process.

## Features
- **Video Processing**: Extract frames from video files for barcode/QR detection.
- **Barcode & QR Code Detection**: Uses OpenCV & pyzbar for scanning.
- **Inventory System Integration**: Updates inventory database in real-time.
- **Web-Based Interface** (Planned): Upload video files via a simple web UI.

## Tech Stack
- **Programming Language**: Python
- **Video Processing**: OpenCV 
- **Barcode Detection**: pyzbar 
- **Database**: SQLite / MySQL 
- **Web Framework (Planned)**: Flask / Streamlit

## Project Structure
barcode-scanner-app  
app.py # Main application script
video_processing.py # Handles video extraction 
barcode_scanner.py # Barcode & QR Code scanning
database.py # Inventory database logic 
requirements.txt # Dependencies 
README.md # Project documentation 
.gitignore # Ignored files (cache, environment)

## Clone the Repository
```bash
git clone https://github.com/seubank96/barcode-scanner-app.git
cd barcode-scanner-app

# Install Dependencies
 pip install -r requirements.txt
```

## Run the Application
```python
python app.py
```

