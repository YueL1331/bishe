import os
import torch
import torchvision.models as models
from torchvision.models.resnet import ResNet50_Weights
from torchvision import transforms
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory, Blueprint
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
api_bp = Blueprint('api', __name__)
IMAGE_DIR = 'api/pictures'  # 存储上传图片的目录
FEATURE_DIR = 'api/features'  # 存储处理后特征文件的目录

# 检查目录是否存在，不存在则创建
for directory in [IMAGE_DIR, FEATURE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weights = ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights).to(device)
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
        for name, layer in self.model.named_children():
            x = layer(x)
            if name in layers:
                outputs[name] = x.detach()
            if all(layer in outputs for layer in layers):
                break
        return outputs


extractor = FeatureExtractor(model)


@api_bp.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = []
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '' or not allowed_file(file.filename):
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(IMAGE_DIR, filename)
        file.save(file_path)
        uploaded_files.append(filename)
        img = Image.open(file_path).convert('RGB')
        img_t = transform(img).unsqueeze(0).to(device)
        features = extractor(img_t)
        for layer, feature_data in features.items():
            feature_array = feature_data.cpu().numpy()
            feature_text = str(feature_array.flatten().tolist())
            layer_dir = os.path.join(FEATURE_DIR, layer)
            if not os.path.exists(layer_dir):
                os.makedirs(layer_dir)
            feature_filename = os.path.join(layer_dir, f"{filename}_{layer}.txt")
            with open(feature_filename, 'w') as f:
                f.write(feature_text)
    return jsonify({'message': 'Images uploaded successfully, features extracted', 'files': uploaded_files})


@api_bp.route('/features/<layer>/<filename>', methods=['GET'])
def get_feature(layer, filename):
    feature_path = os.path.join(FEATURE_DIR, layer, filename)
    if os.path.exists(feature_path):
        return send_from_directory(os.path.join(FEATURE_DIR, layer), filename)
    else:
        return jsonify({'error': 'Feature file not found'}), 404


@api_bp.route('/files/<filename>')
def get_file(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(IMAGE_DIR, filename)
    else:
        return jsonify({'error': 'File not found'}), 404


@api_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    image_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(image_path):
        os.remove(image_path)
        for layer in ['layer1', 'layer2', 'layer3', 'layer4']:
            feature_path = os.path.join(FEATURE_DIR, layer, f"{filename}_{layer}.txt")
            if os.path.exists(feature_path):
                os.remove(feature_path)
        return jsonify({'message': 'File and related features deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404


@api_bp.route('/images', methods=['GET'])
def list_images():
    images = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    return jsonify(images)


app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/')
def home():
    return "Welcome to the Image Feature Extraction API!"


if __name__ == "__main__":
    app.run(debug=True)
