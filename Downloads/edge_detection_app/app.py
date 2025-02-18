import os
from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Set the upload folder for images
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create the upload and output folders if they don't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Edge detection function using OpenCV
def edge_detection(input_image_path, output_image_path):
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)  # Apply Canny edge detection
    cv2.imwrite(output_image_path, edges)  # Save the edge-detected image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        # Secure the file name
        filename = secure_filename(file.filename)
        
        # Save the uploaded image
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_image_path)
        
        # Generate output file name for edge-detected image
        output_filename = 'edges_' + filename
        output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Perform edge detection
        edge_detection(input_image_path, output_image_path)
        
        # Serve the output image
        return render_template('result.html', filename=output_filename)
    
    return 'File not allowed', 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
