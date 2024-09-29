from flask import Flask, request, jsonify, render_template
import os
import torch
from torchvision import transforms
from PIL import Image
from model import SimpleCNN  # Ensure this matches your model definition

app = Flask(__name__)

# Load the trained model
model = SimpleCNN(num_classes=37)  # Ensure this matches your number of classes
model.load_state_dict(torch.load('crop_disease_model.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/predict', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded image
    upload_path = os.path.join('uploads', file.filename)
    file.save(upload_path)

    # Process the image
    img = Image.open(upload_path).convert('RGB')  # Ensure the image is in RGB format
    img = transform(img)  # Apply transformations
    img = img.unsqueeze(0)  # Add batch dimension

    # Make the prediction
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs.data, 1)
        result = predicted.item()  # Get the predicted class

    return jsonify({'prediction': result})  # Return the prediction in a JSON response

if __name__ == '__main__':
    app.run(debug=True)
