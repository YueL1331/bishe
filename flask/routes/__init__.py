# flask/routes/__init__.py

from .SelectScreen import select_screen_bp
from .FeatureExtractionScreen import feature_extraction_screen_bp
# 其他蓝图的导入 ...

# 可选：在这里定义一个函数来统一注册所有蓝图
def register_all_blueprints(app):
    app.register_blueprint(select_screen_bp, url_prefix='/select-screen')
    app.register_blueprint(feature_extraction_screen_bp, url_prefix='/feature-extraction')
    # 其他蓝图的注册 ...
