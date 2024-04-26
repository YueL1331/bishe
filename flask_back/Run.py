from flask import Flask
from flask_cors import CORS

from flask_back.routes.SelectScreen import select_screen_bp
from flask_back.routes.FeatureExtractionScreen import fe_screen_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(select_screen_bp, url_prefix='/api')
app.register_blueprint(fe_screen_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
