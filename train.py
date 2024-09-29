import os
import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from model import SimpleCNN  # Make sure your model architecture is defined here

# Corrected Directories with proper escape sequences or raw string literals
train_dir = r'D:\git2\Crop-Disease-Prediction-AI-\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'
val_dir = r'D:\git2\Crop-Disease-Prediction-AI-\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\valid'

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Add print statements to track dataset loading
print("Loading training dataset...")
train_dataset = datasets.ImageFolder(root=train_dir, transform=transform)
print(f"Training dataset loaded with {len(train_dataset)} images and {len(train_dataset.classes)} classes.")

print("Loading validation dataset...")
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform)
print(f"Validation dataset loaded with {len(val_dataset)} images and {len(val_dataset.classes)} classes.")

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize model, loss function, and optimizer
print("Initializing model...")
model = SimpleCNN(num_classes=len(train_dataset.classes))  # Adjust based on your dataset
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10  # Adjust as needed
print(f"Starting training for {num_epochs} epochs...")
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (images, labels) in enumerate(train_loader, 0):
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        if i % 10 == 9:    # Print every 10 mini-batches
            print(f"[Epoch {epoch + 1}, Batch {i + 1}] loss: {running_loss / 10:.3f}")
            running_loss = 0.0
    
print("Training complete. Saving the model...")
torch.save(model.state_dict(), 'crop_disease_model.pth')  # Saves the trained model
print("Model saved.")
