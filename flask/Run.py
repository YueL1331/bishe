# flask/run.py
from flask import Flask

app = Flask(__name__)

# 可能需要从其他地方导入和注册路由
from .routes.SelectScreen import select_screen_bp
app.register_blueprint(select_screen_bp)

if __name__ == '__main__':
    app.run(debug=True)
