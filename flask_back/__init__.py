# flask_back/__init__.py

from flask import Flask
from flask_cors import CORS
from .routes import register_all_blueprints


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    @app.route('/')
    def home():
        return "Hello, Flask is running!"

    register_all_blueprints(app)

    return app
