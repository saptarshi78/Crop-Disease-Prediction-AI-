from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from PIL import Image

app = Flask(__name__)

# Load your pre-trained AI model (you can train it separately or use a pre-trained one)
model = load_model('path_to_your_model.h5')

# Function to preprocess the image
def preprocess_image(image):
    # Resize the image to the input size of the model (change this according to your model)
    image = image.resize((224, 224))  # Example size, adjust as necessary
    image = np.array(image)
    image = image / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)
    return image

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image uploads
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    try:
        # Read the image using PIL and preprocess it
        image = Image.open(file)
        preprocessed_image = preprocess_image(image)

        # Get predictions from the model
        predictions = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions[0])

        # Convert the result into a meaningful label (adjust based on your dataset)
        labels = ['Healthy', 'Disease 1', 'Disease 2', 'Disease 3']
        result = labels[predicted_class]

        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
