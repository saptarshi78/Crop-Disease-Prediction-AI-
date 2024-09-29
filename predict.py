import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from model import SimpleCNN  # Make sure your model architecture is defined here

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Adjust size as per your model's input
    transforms.ToTensor(),
])

# Load the trained model
model = SimpleCNN(num_classes=37)  # Make sure num_classes matches your training
model.load_state_dict(torch.load('crop_disease_model.pth'))
model.eval()

# Function to make predictions
def predict(image_path):
    # Load the image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Make the prediction
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output.data, 1)
    
    return predicted.item()

# Example usage
if __name__ == "__main__":
    # Change this path to the image you want to predict
    test_image_path = 'path_to_your_test_image.jpg'
    prediction = predict(test_image_path)
    print(f'Predicted class: {prediction}')
