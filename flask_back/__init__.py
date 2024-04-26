# flask_back/__init__.py

from flask import Flask
from .routes import register_all_blueprints  # 导入你刚定义的函数


def create_app():
    app = Flask(__name__)

    # 使用一个函数调用注册所有蓝图
    register_all_blueprints(app)

    return app
