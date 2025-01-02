from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Config 파일이 설정되는 부분
    app.register_blueprint(main)
    return app