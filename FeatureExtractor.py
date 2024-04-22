import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image

# 设定模型和设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from torchvision.models import resnet50, ResNet50_Weights
model = resnet50(weights=ResNet50_Weights.DEFAULT).to(device)
model.eval()

# 图像转换
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

    def forward(self, x, layers):
        outputs = {}
        for name, layer in self.model.named_children():
            x = layer(x)
            if name in layers:
                outputs[name] = x.detach()  # 使用detach()来避免计算图的保存
            if all(layer in outputs for layer in layers):
                break
        return outputs

# 实例化提取器
extractor = FeatureExtractor(model)

def process_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img_t = transform(img).unsqueeze(0).to(device)
    return extractor(img_t, ['layer1', 'layer2', 'layer3', 'layer4'])


def process_image(image_path):
    """处理图像并返回所选层的特征"""
    img = Image.open(image_path).convert('RGB')
    img_t = transform(img).unsqueeze(0).to(device)
    features = extractor(img_t)  # 获取特征
    return features
