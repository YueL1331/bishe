from flask import Flask, request, jsonify, send_from_directory, Blueprint, current_app
import os
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
from werkzeug.utils import secure_filename
from torchvision.models.resnet import ResNet50_Weights
import numpy as np
import cv2
import glob

app = Flask(__name__)
api_bp = Blueprint('api', __name__)

IMAGE_DIR = 'api/pictures'
FEATURE_DIR = 'api/features'
OUTPUT_DIR = 'api/stitched_images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
if not os.path.exists(FEATURE_DIR):
    os.makedirs(FEATURE_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

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
    try:
        for file_key in request.files:
            file = request.files[file_key]
            if file.filename == '' or not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in {'jpg',
                                                                                                                  'jpeg',
                                                                                                                  'png'}:
                continue
            filename = secure_filename(file.filename)
            file_path = os.path.join(IMAGE_DIR, filename)
            file.save(file_path)
            uploaded_files.append(filename)
            current_app.logger.info(f"File saved to {file_path}")
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
                current_app.logger.info(f"Feature for {filename} in {layer} saved.")
        for layer in extractor.selected_layers:
            for batch_size, step_size in [(10, 10), (10, 15), (15, 15), (15, 10)]:
                process_feature_directory(os.path.join(FEATURE_DIR, layer), batch_size, step_size)
        return jsonify({'message': 'Images uploaded and features extracted, stitching initiated for all combinations.',
                        'files': uploaded_files})
    except Exception as e:
        current_app.logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500


def load_feature_vectors_and_sort(feature_dir):
    vectors = {}
    for feature_file in glob.glob(os.path.join(feature_dir, '*.txt')):
        with open(feature_file, 'r') as file:
            content = file.read().strip()
            vector = np.array([float(num) for num in content.strip('[]').split(',')])
            image_name = os.path.basename(feature_file).replace('.txt', '').rsplit('_', 1)[0]
            vectors[image_name] = vector

    if not vectors:
        return []

    reference_vector = vectors[list(vectors.keys())[0]]
    sorted_image_names = sorted(vectors.keys(), key=lambda x: np.linalg.norm(vectors[x] - reference_vector))
    return sorted_image_names


def stitch_images(images):
    if len(images) < 2:
        print("Not enough images to stitch")
        return None

    stitcher = cv2.Stitcher_create() if hasattr(cv2, 'Stitcher_create') else cv2.createStitcher()
    status, stitched = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        return stitched
    else:
        print(f"Stitching failed with status: {status}")
        return None


def process_feature_directory(feature_dir, batch_size=10, step_size=10):
    current_app.logger.info(
        f"Processing feature directory: {feature_dir} with batch_size: {batch_size} and step_size: {step_size}")
    sorted_image_names = load_feature_vectors_and_sort(feature_dir)

    if not sorted_image_names:
        current_app.logger.warning(f"No valid feature vectors found in {feature_dir}")
        return

    output_dir = os.path.join(OUTPUT_DIR, f"{batch_size}_{step_size}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    batch_stitched_images = []
    for i in range(0, len(sorted_image_names), step_size):
        batch = sorted_image_names[i:i + batch_size]
        images = []
        for name in batch:
            img_path = os.path.join(IMAGE_DIR, name)
            if os.path.isfile(img_path):
                img = cv2.imread(img_path)
                if img is not None:
                    images.append(img)
                else:
                    current_app.logger.warning(f"Failed to read image: {img_path}")
            else:
                current_app.logger.warning(f"Image file not found: {img_path}")

        if images:
            stitched_image = stitch_images(images)
            if stitched_image is not None:
                batch_stitched_images.append(stitched_image)
            else:
                current_app.logger.warning(f"Failed to stitch batch starting with {batch[0]}")
        else:
            current_app.logger.warning(f"No valid images found for batch starting with {batch[0]}")

    if batch_stitched_images:
        final_stitched = stitch_images(batch_stitched_images)
        if final_stitched is not None:
            layer_name = os.path.basename(feature_dir)
            output_filepath = os.path.join(output_dir, f"{layer_name}_{batch_size}_{step_size}.png")
            cv2.imwrite(output_filepath, final_stitched)
            current_app.logger.info(f'Stitched final image saved to {output_filepath}')
        else:
            current_app.logger.warning(f'Failed to stitch final image for {feature_dir}')
    else:
        current_app.logger.warning(f'No batches stitched for {feature_dir}')


@api_bp.route('/stitch/all_layers', methods=['GET'])
def get_all_layers_stitched_images():
    results = {}
    for batch_size, step_size in [(10, 10), (10, 15), (15, 15), (15, 10)]:
        output_dir = os.path.join(OUTPUT_DIR, f"{batch_size}_{step_size}")
        for layer in ['layer1', 'layer2', 'layer3', 'layer4']:
            output_filepath = f"{layer}_{batch_size}_{step_size}.png"
            output_path = os.path.join(output_dir, output_filepath)
            if os.path.exists(output_path):
                image_url = request.host_url.rstrip(
                    '/') + '/api/stitched_images/' + f"{batch_size}_{step_size}/" + output_filepath
                results[f"{layer}_{batch_size}_{step_size}"] = image_url
            else:
                results[f"{layer}_{batch_size}_{step_size}"] = None

    if all(value is None for value in results.values()):
        return jsonify({'error': 'No stitched images found for the given parameters'}), 404

    return jsonify(results)


@api_bp.route('/stitched_images/<batch_size>_<step_size>/<filename>', methods=['GET'])
def serve_stitched_image(batch_size, step_size, filename):
    file_directory = os.path.join(OUTPUT_DIR, f"{batch_size}_{step_size}")
    file_path = os.path.join(file_directory, filename)

    if os.path.exists(file_path):
        return send_from_directory(file_directory, filename)
    else:
        error_url = request.host_url.rstrip('/') + '/static/error.jpg'
        return jsonify({'url': error_url})


@api_bp.route('/stitched_images', methods=['GET'])
def list_all_stitched_images():
    results = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith('.png'):  # 只包括 PNG 文件
                file_path = os.path.join(root, file)
                file_url = request.host_url.rstrip('/') + '/' + file_path.replace('\\', '/')
                results.append(file_url)
    return jsonify(results)


@app.route('/test_static/<path:filename>')
def test_static(filename):
    return send_from_directory(app.static_folder, filename)


# 确保 /api/files 路由正确注册在 Flask 应用中
@api_bp.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(IMAGE_DIR)  # 直接从 IMAGE_DIR 获取文件列表
    return jsonify({'files': files})


@api_bp.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        file_path = os.path.join(IMAGE_DIR, filename)
        if os.path.exists(file_path):
            return send_from_directory(IMAGE_DIR, filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving file {filename}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        image_path = os.path.join(IMAGE_DIR, filename)
        if os.path.exists(image_path):
            os.remove(image_path)
            for layer in ['layer1', 'layer2', 'layer3', 'layer4']:
                feature_path = os.path.join(FEATURE_DIR, layer, f"{filename.rsplit('.', 1)[0]}_{layer}.txt")
                if os.path.exists(feature_path):
                    os.remove(feature_path)
            current_app.logger.info(f"File and associated features successfully deleted: {filename}")
            return jsonify({'message': f'File {filename} and associated features deleted'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error deleting file {filename}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/features/<layer>/<filename>')
def get_feature_file(layer, filename):
    feature_path = os.path.join(FEATURE_DIR, layer, filename)
    if os.path.exists(feature_path):
        return send_from_directory(os.path.join(FEATURE_DIR, layer), filename)
    else:
        return jsonify({'error': 'Feature file not found'}), 404


@api_bp.route('/delete_feature/<layer>/<filename>', methods=['DELETE'])
def delete_feature_file(layer, filename):
    feature_path = os.path.join(FEATURE_DIR, layer, filename)
    if os.path.exists(feature_path):
        os.remove(feature_path)
        return jsonify({'message': 'Feature file deleted successfully'}), 200
    else:
        return jsonify({'error': 'Feature file not found'}), 404


@api_bp.route('/images', methods=['GET'])
def list_images():
    images = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    return jsonify(images)


# 注册 Blueprint
app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/')
def home():
    return "Welcome to the Image Feature Extraction API!"


if __name__ == "__main__":
    app.run(debug=True)
