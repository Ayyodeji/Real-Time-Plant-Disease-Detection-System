from flask import Flask, render_template, request, jsonify
import numpy as np
import base64
import cv2
from keras.models import load_model
import boto3

# Initialize the S3 client
s3_client = boto3.client('s3')

# Download the model file from S3
model_file_key = 'PDD/model.h5'
local_model_path = '/PDD/ec2/model.h5'
s3_client.download_file('PDD-s3-bucket', model_file_key, local_model_path)
loaded_model = load_model(local_model_path)
app = Flask(__name__)

# Load the trained model
trained_model = load_model('./model/PDDCNN.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    frame_data = request.json.get('frame_data')
    frame = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)
    resized_frame = cv2.resize(frame, (80, 80))  # Adjust dimensions as needed
    normalized_frame = resized_frame / 255.0
    input_data = np.expand_dims(normalized_frame, axis=0)
    predictions = trained_model.predict(input_data)
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class]
    class_names = ['Healthy', 'Powdery', 'Rust']  # Replace with your class names
    class_label = class_names[predicted_class]
    result = {'class': class_label, 'confidence': confidence}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
