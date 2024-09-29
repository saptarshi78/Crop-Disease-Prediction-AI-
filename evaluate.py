import os
import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn as nn
from model import SimpleCNN  # Ensure your model architecture is defined here

# Directories for the validation dataset
val_dir = r'D:\git2\Crop-Disease-Prediction-AI-\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\valid'

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load validation dataset
print("Loading validation dataset...")
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Load the trained model
print("Initializing model...")
model = SimpleCNN(num_classes=len(val_dataset.classes))  # Adjust based on your dataset
model.load_state_dict(torch.load('crop_disease_model.pth'))
model.eval()

correct = 0
total = 0
num_batches = len(val_loader)

print("Evaluating the model...")

with torch.no_grad():
    for batch_idx, (images, labels) in enumerate(val_loader):
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        # Print live progress every 10 batches
        if (batch_idx + 1) % 10 == 0 or (batch_idx + 1) == num_batches:
            print(f'Processed {batch_idx + 1}/{num_batches} batches.')

# Calculate accuracy
accuracy = 100 * correct / total
print(f'Validation Accuracy: {accuracy:.2f}%')
