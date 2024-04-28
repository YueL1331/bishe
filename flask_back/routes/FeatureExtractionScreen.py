import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import torch
import torchvision.models as models
from torchvision.models.resnet import ResNet50_Weights
from torchvision import transforms
from PIL import Image

# 定义蓝图
feature_extraction_screen_bp = Blueprint('fe_screen', __name__)

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型，使用最新的权重参数
weights = ResNet50_Weights.DEFAULT  # 默认权重通常是最新的预训练权重
model = models.resnet50(weights=weights).to(device)
model.eval()

# 定义图像转换
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
                outputs[name] = x.detach()
            if all(layer in outputs for layer in layers):
                break
        return outputs


extractor = FeatureExtractor(model)


# 定义特征提取的路由
@feature_extraction_screen_bp.route('/feature', methods=['POST'])
def get_feature():
    file = request.files['file']
    layer = request.form['layer']

    try:
        img = Image.open(file).convert('RGB')
        img_t = transform(img).unsqueeze(0).to(device)
        features = extractor(img_t, [layer])
        feature_text = str(features[layer].flatten().tolist())
        return jsonify({'feature': feature_text})
    except Exception as e:
        return jsonify({'error': 'Failed to process image or extract features due to: ' + str(e)}), 500


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(feature_extraction_screen_bp, url_prefix='/api')

    # 添加根路径响应
    @app.route('/')
    def home():
        return "Welcome to the Image Feature Extraction API!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
