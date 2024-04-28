from flask import Flask, request, jsonify, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
import os
import tempfile

app = Flask(__name__)
select_screen_bp = Blueprint('SelectScreen', __name__)
# 创建一个临时目录用于存储上传的文件
temp_dir = tempfile.mkdtemp()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


@app.route('/api/upload', methods=['POST'])  # 确保路径匹配
def upload_files():
    uploaded_files = []
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            uploaded_files.append(filename)
    if uploaded_files:
        return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files})
    else:
        return jsonify({'error': 'No valid files uploaded'}), 400


@app.route('/files/<filename>')
def get_file(filename):
    if os.path.exists(os.path.join(temp_dir, filename)):
        return send_from_directory(temp_dir, filename)
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        os.remove(file_path)
    return jsonify({'message': 'Temporary files cleaned up'})


print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
