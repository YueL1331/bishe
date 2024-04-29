# flask_back/routes/__init__.py

from .SelectScreen import select_screen_bp
from .FeatureExtractionScreen import feature_extraction_screen_bp


def register_all_blueprints(app):
    app.register_blueprint(select_screen_bp, url_prefix='/api')
    app.register_blueprint(feature_extraction_screen_bp, url_prefix='/api')
