from flask import Flask, request, jsonify, send_from_directory, Blueprint, current_app
import os
import cv2
import numpy as np
import glob
from werkzeug.utils import secure_filename
from PIL import Image
import torch
from torchvision import transforms
import torchvision.models as models
from torchvision.models.resnet import ResNet50_Weights
import gc  # 垃圾收集器接口

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


@api_bp.route('/feature', methods=['POST'])
def get_feature():
    file = request.files['file']
    layer = request.form['layer']
    base_dir = 'api/features'
    if not os.path.exists(FEATURE_DIR):
        os.makedirs(FEATURE_DIR)
    layer_dir = os.path.join(FEATURE_DIR, layer)
    if not os.path.exists(layer_dir):
        os.makedirs(layer_dir)

    filename = secure_filename(file.filename)

    try:
        img = Image.open(file).convert('RGB')
        img_t = transform(img).unsqueeze(0).to(device)
        features = extractor(img_t, [layer])
        feature_array = features[layer].cpu().numpy()
        feature_text = str(feature_array.flatten().tolist())
        feature_filename = os.path.join(layer_dir, f"{filename.rsplit('.', 1)[0]}_{layer}.txt")
        with open(feature_filename, 'w') as f:
            f.write(feature_text)
        current_app.logger.info(f"Feature for {filename} in {layer} saved.")
        return jsonify({'feature': feature_text, 'saved_to': feature_filename})
    except Exception as e:
        current_app.logger.error(f"Failed to process image or extract features due to: {str(e)}")
        return jsonify({'error': str(e)}), 500


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
        batch_and_step_combinations = [(10, 10), (10, 15), (15, 15), (15, 10)]
        for layer in extractor.selected_layers:
            for batch_size, step_size in batch_and_step_combinations:
                stitch_result = stitch_images(layer, batch_size, step_size)
                current_app.logger.info(
                    f"Stitching result for layer {layer} with batch size {batch_size} and step size {step_size}: {stitch_result}")
        return jsonify({'message': 'Images uploaded and features extracted, stitching initiated for all combinations.',
                        'files': uploaded_files})
    except Exception as e:
        current_app.logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500


def round_and_save_feature_files(layer_dir, decimal_places=17):
    for feature_file in glob.glob(os.path.join(layer_dir, '*.txt')):
        with open(feature_file, 'r') as file:
            content = file.read().strip()
            content = content.replace('[', '').replace(']', '')
            vector = np.array(list(map(float, content.split(','))))

        rounded_vector = np.round(vector, decimal_places)
        with open(feature_file, 'w') as file:
            feature_text = '[' + ', '.join(f"{num:.17f}" for num in rounded_vector) + ']'
            file.write(feature_text)


def stitch_images(layer, batch_size, step_size):
    feature_dir = os.path.join(FEATURE_DIR, layer)
    image_dir = IMAGE_DIR
    output_dir = os.path.join(OUTPUT_DIR, f"{batch_size}_{step_size}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    round_and_save_feature_files(feature_dir)

    output_filepath = f"{layer}_{batch_size}_{step_size}.png"
    output_path = os.path.join(output_dir, output_filepath)

    if not os.path.exists(output_path):
        images = load_and_stitch_images(feature_dir, image_dir, batch_size, step_size)
        if images is not None:
            cv2.imwrite(output_path, images)
            # 删除中间虚拟文件
            for feature_file in glob.glob(os.path.join(feature_dir, '*.txt')):
                os.remove(feature_file)
            gc.collect()
            return "Success"
        else:
            return "Failed"
    return "Image already exists"


def load_and_stitch_images(feature_dir, image_dir, batch_size, step_size):
    sorted_image_names = load_feature_vectors_and_sort(feature_dir)
    batches = [sorted_image_names[i:i + batch_size] for i in range(0, len(sorted_image_names), step_size)]
    batch_stitched_images = []

    for batch in batches:
        images = []
        for feature_filename in batch:
            # 提取原始图像文件名，假设特征向量文件名格式为 'split_0.png_layer4.txt'
            original_image_filename = feature_filename.split('_layer')[0]  # 已经包含 '.png'
            image_path = os.path.join(image_dir, original_image_filename)
            if os.path.isfile(image_path):
                img = cv2.imread(image_path)
                if img is not None:
                    images.append(img)
        stitched_image = stitch_one_batch(images)
        if stitched_image is not None:
            batch_stitched_images.append(stitched_image)
        # 处理每个批次后清除内存
        del images
        gc.collect()

    final_stitched = stitch_one_batch(batch_stitched_images)
    # 清理批处理图像内存
    del batch_stitched_images
    gc.collect()
    return final_stitched


def stitch_one_batch(images):
    stitcher = cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        return stitched
    else:
        current_app.logger.error(f"Image stitching failed, status code: {status}")
        if status == cv2.Stitcher_ERR_NEED_MORE_IMGS:
            current_app.logger.error("Need more images for stitching.")
        elif status == cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL:
            current_app.logger.error("Homography estimation failed.")
        elif status == cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL:
            current_app.logger.error("Camera parameters adjustment failed.")
        return None


def load_feature_vectors_and_sort(feature_dir):
    vectors = {}
    for feature_file in glob.glob(os.path.join(feature_dir, '*.txt')):
        with open(feature_file, 'r') as file:
            content = file.read().strip()
            content = content.replace('[', '').replace(']', '')
            vector = np.array(list(map(float, content.split(','))))
            image_name = os.path.basename(feature_file).replace('.txt', '.png')
            vectors[image_name] = vector
    if not vectors:
        return []
    reference_vector = next(iter(vectors.values()))
    sorted_image_names = sorted(vectors.keys(), key=lambda x: np.linalg.norm(vectors[x] - reference_vector))
    return sorted_image_names


@api_bp.route('/stitch/all_layers', methods=['GET'])
def get_all_layers_stitched_images():
    batch_size = request.args.get('batch_size')
    step_size = request.args.get('step_size')
    if not batch_size or not step_size:
        return jsonify({'error': 'Missing batch_size or step_size'}), 400

    results = {}
    output_dir = os.path.join(OUTPUT_DIR, f"{batch_size}_{step_size}")
    for layer in ['layer1', 'layer2', 'layer3', 'layer4']:
        output_filepath = f"{layer}_{batch_size}_{step_size}.png"
        output_path = os.path.join(output_dir, output_filepath)
        if os.path.exists(output_path):
            # 生成图像的完整URL
            image_url = request.host_url + 'api/' + os.path.relpath(output_path, start=os.getcwd())
            results[layer] = image_url
        else:
            results[layer] = None  # 没有找到图像时返回None

    if all(value is None for value in results.values()):
        return jsonify({'error': 'No stitched images found for the given parameters'}), 404

    return jsonify(results)


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
                feature_path = os.path.join(FEATURE_DIR, layer, f"{filename}_{layer}.txt")
                if os.path.exists(feature_path):
                    os.remove(feature_path)
            current_app.logger.info(f"文件及相关特征已成功删除 {filename}")
            gc.collect()  # 在删除文件后触发垃圾收集
            return jsonify({'message': '文件及相关特征已成功删除'}), 200
        else:
            return jsonify({'error': '文件未找到'}), 404
    except Exception as e:
        current_app.logger.error(f"删除文件 {filename} 时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/features/<layer>/<filename>')
def get_feature_file(layer, filename):
    # 生成完整的文件路径应该包括层级和文件名
    feature_path = os.path.join(FEATURE_DIR, layer, filename)
    if os.path.exists(feature_path):
        return send_from_directory(os.path.join(FEATURE_DIR, layer), filename)
    else:
        return jsonify({'error': 'Feature file not found'}), 404


@api_bp.route('/delete_feature/<layer>/<filename>', methods=['DELETE'])
def delete_feature_file(filename):
    feature_path = os.path.join(FEATURE_DIR, filename)
    if os.path.exists(feature_path):
        os.remove(feature_path)
        return jsonify({'message': 'Feature file deleted successfully'}), 200
    else:
        return jsonify({'error': 'Feature file not found'}), 404


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
