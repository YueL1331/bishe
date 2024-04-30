from flask import Flask, request, jsonify, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
select_screen_bp = Blueprint('SelectScreen', __name__)
IMAGE_DIR = 'api/pictures'  # 定义图片存储的目录

# 检查存储目录是否存在，如果不存在则创建
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


@select_screen_bp.route('/picture', methods=['POST'])
def upload_files():
    uploaded_files = []
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(IMAGE_DIR, filename)
            file.save(file_path)  # Always save/overwrite the file
            uploaded_files.append(filename)
            print(f"File saved/overwritten: {filename}")
    if uploaded_files:
        return jsonify({'message': '图像上传成功', 'files': uploaded_files})
    else:
        return jsonify({'error': '没有上传成功'}), 400


@select_screen_bp.route('/files/<filename>')
def get_file(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(IMAGE_DIR, filename)
    else:
        return jsonify({'error': 'File not found'}), 404


@select_screen_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
