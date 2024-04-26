from flask import Flask
from flask_cors import CORS
from SelectScreen import select_screen_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(select_screen_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
