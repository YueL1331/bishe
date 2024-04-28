from flask import Flask
from flask_cors import CORS

from flask_back.routes.SelectScreen import select_screen_bp
from flask_back.routes.FeatureExtractionScreen import feature_extraction_screen_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

app.register_blueprint(select_screen_bp, url_prefix='/api')
app.register_blueprint(feature_extraction_screen_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=8081, host='0.0.0.0')
