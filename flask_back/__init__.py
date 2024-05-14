# flask_back/__init__.py
import os

from flask import Flask, jsonify
from flask_cors import CORS
from .routes import register_all_blueprints
import urllib


def create_app():
    app = Flask(__name__, static_folder='static')  # 指定静态文件目录
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.route('/')
    def home():
        return "Hello, Flask is running!"

    register_all_blueprints(app)

    @app.route("/show_routes", methods=["GET"])
    def show_routes():
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = f"[{arg}]"
            methods = ','.join(rule.methods)
            url = urllib.parse.unquote(f"{rule}")
            line = urllib.parse.unquote(f"{methods} {url}")
            output.append(line)
        return jsonify(sorted(output))

    @app.route('/debug/static_path')
    def debug_static_path():
        return os.path.abspath(app.static_folder)

    return app
