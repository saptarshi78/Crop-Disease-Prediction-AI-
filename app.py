from flask import Flask, render_template, request, jsonify
import tensorflow as tf
#from tensorflow.keras.models import load_model # type: ignore
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load your pre-trained AI model (adjust the path accordingly)
#model = load_model('path_to_your_model.h5')

def preprocess_image(image):
    image = image.resize((224, 224))  # Adjust based on your model
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

   # try:
       # image = Image.open(file)
         #preprocessed_image = preprocess_image(image)
        #predictions = model.predict(preprocessed_image) # type: ignore
        #predicted_class = np.argmax(predictions[0])
        #labels = ['Healthy', 'Disease 1', 'Disease 2', 'Disease 3']  # Adjust as necessary
        #result = labels[predicted_class]
        #return jsonify({"prediction": result})
    #except Exception as e:
      # return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
