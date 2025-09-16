from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Folders and files
UPLOAD_FOLDER = './uploaded_images'
CSV_LOG = 'status_log.csv'

# Create folders and files if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to initialize CSV log
def initialize_csv_log():
    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Name', 'Camera Status', 'CPU Temperature', 'Power Status'])

# Function to save the image
def save_image(image_file):
    if image_file and image_file.filename != '':
        image_filename = image_file.filename
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)
        print(f"Image saved to {image_path}")
        return image_filename
    return "N/A"

# Function to log data to CSV
def log_to_csv(image_filename, camera_status, cpu_temperature, power_status):
    with open(CSV_LOG, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([camera_status, cpu_temperature, power_status])

# Route for the home page
@app.route('/')
def home():
    return "Flask server is running!"

# Route to handle image upload and logging
@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the image file
    image_file = request.files.get('file')
    image_filename = save_image(image_file)

    # Get status data
    camera_status = request.form.get('camera_status', 'N/A')
    cpu_temperature = request.form.get('cpu_temperature', 'N/A')
    power_status = request.form.get('power_status', 'N/A')

    # Log the data
    log_to_csv(image_filename, camera_status, cpu_temperature, power_status)

    # Console log
    print(f"Camera status: {camera_status}")
    print(f"CPU temperature: {cpu_temperature}°C")
    print(f"Power status: {power_status}")

    return jsonify({
        "message": "Image and status logged successfully!",
        "file": image_filename
    }), 200

if __name__ == '__main__':
    initialize_csv_log()  # Initialize the CSV file before starting the server
    app.run(debug=True, host='0.0.0.0', port=5000)
