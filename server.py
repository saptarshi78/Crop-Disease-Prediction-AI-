from flask import Flask, request, jsonify
import torch
from torchvision import transforms
from PIL import Image
from model import SimpleCNN  # Import your model architecture here

app = Flask(__name__)

# Load the model
model = SimpleCNN(num_classes=37)  # Update to match your number of classes
model.load_state_dict(torch.load('crop_disease_model.pth', weights_only=True))
model.eval()  # Set model to evaluation mode

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    
    try:
        # Load the image
        image = Image.open(file.stream).convert('RGB')
        image = transform(image).unsqueeze(0)  # Add batch dimension

        # Make prediction
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            predicted_class = predicted.item()  # Get the predicted class index

        return jsonify({'predicted_class': predicted_class})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
