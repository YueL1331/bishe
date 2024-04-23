# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import uuid
#
# app = Flask(__name__)
# CORS(app)  # 允许所有域的跨域请求
#
# # 配置上传文件夹
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# # 确保上传文件夹存在
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     if 'images' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     files = request.files.getlist('images')
#     image_urls = []
#     for file in files:
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         if file and allowed_file(file.filename):
#             filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#             image_url = f'/uploads/{filename}'
#             image_urls.append({'url': image_url, 'id': filename})
#     return jsonify({'images': image_urls}), 200
#
# @app.route('/api/images/<filename>', methods=['DELETE'])
# def delete_file(filename):
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         return jsonify({'status': 'success'}), 200
#     else:
#         return jsonify({'error': 'File not found'}), 404
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
#
# if __name__ == '__main__':
#     app.run(debug=True)
