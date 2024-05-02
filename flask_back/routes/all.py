import os
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, Blueprint
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import torch
import torchvision.models as models
from torchvision.models.resnet import ResNet50_Weights
from torchvision import transforms
from PIL import Image

app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__)
IMAGE_DIR = 'api/pictures'  # 存储上传图片的目录
FEATURE_DIR = 'api/layers'  # 存储处理后特征文件的目录

# 检查目录是否存在，不存在则创建
for directory in [IMAGE_DIR, FEATURE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)


# 检查文件是否为允许的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


# 定义设备（CPU或GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型
weights = ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights).to(device)
model.eval()

# 定义图像转换
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


# 定义特征提取器
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


# 路由处理特征提取
@api_bp.route('/feature', methods=['POST'])
def get_feature():
    file = request.files['file']
    layer = request.form['layer']
    base_dir = 'api/layers'  # 基本目录

    # 确保特征目录存在
    if not os.path.exists(FEATURE_DIR):
        os.makedirs(FEATURE_DIR)
    layer_dir = os.path.join(FEATURE_DIR, layer)
    if not os.path.exists(layer_dir):
        os.makedirs(layer_dir)

    try:
        # 处理图片
        img = Image.open(file).convert('RGB')
        img_t = transform(img).unsqueeze(0).to(device)
        features = extractor(img_t, [layer])

        # 保存特征为文本文件
        feature_array = features[layer].cpu().numpy()
        feature_text = str(feature_array.flatten().tolist())
        feature_filename = os.path.join(layer_dir, f"{secure_filename(file.filename).rsplit('.', 1)[0]}_{layer}.txt")
        with open(feature_filename, 'w') as f:
            f.write(feature_text)

        return jsonify({'feature': feature_text, 'saved_to': feature_filename})
    except Exception as e:
        return jsonify({'error': 'Failed to process image or extract features due to: ' + str(e)}), 500


# 路由处理图片上传
@api_bp.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = []
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(IMAGE_DIR, filename)
            file.save(file_path)
            uploaded_files.append(filename)
            print(f"File saved/overwritten: {filename}")
    if uploaded_files:
        return jsonify({'message': '图像上传成功', 'files': uploaded_files})
    else:
        return jsonify({'error': '没有上传成功'}), 400


@api_bp.route('/files/<filename>')
def get_file(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(IMAGE_DIR, filename)
    else:
        return jsonify({'error': 'File not found'}), 404


# 路由处理图片删除
@api_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    image_path = os.path.join(IMAGE_DIR, filename)
    feature_path = os.path.join(FEATURE_DIR, filename.rsplit('.', 1)[0] + '_layer.npy')
    if os.path.exists(image_path):
        os.remove(image_path)
        if os.path.exists(feature_path):
            os.remove(feature_path)
        return jsonify({'message': '文件删除成功'}), 200
    else:
        return jsonify({'error': '文件未找到'}), 404


@api_bp.route('/features/<filename>')
def get_feature_file(filename):
    feature_path = os.path.join(FEATURE_DIR, filename)
    if os.path.exists(feature_path):
        return send_from_directory(FEATURE_DIR, filename)
    else:
        return jsonify({'error': 'Feature file not found'}), 404


@api_bp.route('/delete_feature/<filename>', methods=['DELETE'])
def delete_feature_file(filename):
    feature_path = os.path.join(FEATURE_DIR, filename)
    if os.path.exists(feature_path):
        os.remove(feature_path)
        return jsonify({'message': 'Feature file deleted successfully'}), 200
    else:
        return jsonify({'error': 'Feature file not found'}), 404


# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')


# 主页路由
@app.route('/')
def home():
    return "欢迎使用图像特征提取API!"


if __name__ == "__main__":
    app.run(debug=True)
