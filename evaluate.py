import os
import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn as nn
from model import SimpleCNN  # Ensure your model architecture is defined here

# Corrected Directories with proper escape sequences or raw string literals
val_dir = r'D:\git2\Crop-Disease-Prediction-AI-\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\valid'

# Image transformations (same as training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load validation dataset
print("Loading validation dataset...")
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform)
print(f"Validation dataset loaded with {len(val_dataset)} images and {len(val_dataset.classes)} classes.")

val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Load the trained model
print("Initializing model...")
model = SimpleCNN(num_classes=len(val_dataset.classes))  # Ensure num_classes matches the training
model.load_state_dict(torch.load('crop_disease_model.pth'))
model.eval()

correct = 0
total = 0

# Evaluate the model
with torch.no_grad():
    print("Evaluating the model...")
    for images, labels in val_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

# Calculate accuracy
accuracy = 100 * correct / total
print(f'Validation Accuracy: {accuracy:.2f}%')
