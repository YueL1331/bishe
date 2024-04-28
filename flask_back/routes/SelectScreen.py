from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os


# 设置蓝图
select_screen_bp = Blueprint('select_screen', __name__)

# 上传文件夹的路径
UPLOAD_FOLDER = 'path/to/uploads'
# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 文件类型验证函数
def allowed_file(filename):
    """
    验证文件扩展名是否在允许的类型中
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


@select_screen_bp.route('/upload', methods=['POST'])
def upload_files():
    """
    处理文件上传请求
    """
    files = request.files.getlist('file')  # 获取所有文件列表

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    uploaded_files = []  # 用于存储上传成功的文件路径
    errors = []  # 用于存储遇到的错误

    for file in files:
        if file.filename == '':
            errors.append('Some files did not have a filename')
            continue

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 安全地获取文件名
            file_path = os.path.join(UPLOAD_FOLDER, filename)  # 定义文件路径
            file.save(file_path)  # 保存文件
            uploaded_files.append(file_path)  # 添加到上传成功列表
        else:
            errors.append(f'{file.filename}: Invalid file type')

    if errors:
        return jsonify({'error': 'No valid files were uploaded', 'details': errors}), 400

    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files}), 200
