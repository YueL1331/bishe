import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from torchvision.models import resnet50, ResNet50_Weights
model = resnet50(weights=ResNet50_Weights.DEFAULT).to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class FeatureExtractor(torch.nn.Module):
    def __init__(self, model):
        super(FeatureExtractor, self).__init__()
        self.model = model
        self.selected_layers = ['layer1', 'layer2', 'layer3', 'layer4']

    def forward(self, x, layers=None):
        if layers is None:
            layers = self.selected_layers
        outputs = {}
        for name, module in self.model.named_children():
            x = module(x)
            if name in layers:
                outputs[name] = x.detach()
            if all(layer in outputs for layer in layers):
                break
        return outputs

extractor = FeatureExtractor(model)

def process_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img_t = transform(img).unsqueeze(0).to(device)
    features = extractor(img_t)
    return features

def save_features(image_path, features):
    base_path = os.path.dirname(image_path)
    feature_dir = os.path.join(base_path, 'FeatureExtractor')
    if not os.path.exists(feature_dir):
        os.makedirs(feature_dir)

    for layer_name, feature in features.items():
        feature_path = os.path.join(feature_dir, f"{layer_name}.npy")
        np.save(feature_path, feature.cpu().numpy())
