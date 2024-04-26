from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

select_screen_bp = Blueprint('select_screen', __name__)

UPLOAD_FOLDER = 'path/to/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@select_screen_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith(('jpg', 'jpeg', 'png')):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File uploaded successfully'}), 200

    return jsonify({'error': 'Invalid file type'}), 400
