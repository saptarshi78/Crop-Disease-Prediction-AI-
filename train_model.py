# train.py
import os
import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from model import SimpleCNN  # Make sure your model architecture is defined here

# Directories
train_dir = os.path.join('D:', 'Crop', 'New Plant Diseases Dataset(Augmented', 'New Plant Diseases Dataset(Augmented', 'train')  # Adjust the path to your training data
val_dir = os.path.join('D:', 'Crop', 'New Plant Diseases Dataset(Augmented', 'New Plant Diseases Dataset(Augmented', 'valid')     # Adjust the path to your validation data

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load datasets
train_dataset = datasets.ImageFolder(root=train_dir, transform=transform)
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize model, loss function, and optimizer
model = SimpleCNN(num_classes=len(train_dataset.classes))  # Adjust based on your dataset
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10  # Adjust as needed
for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Save the model
torch.save(model.state_dict(), 'crop_disease_model.pth')  # Saves the trained model
