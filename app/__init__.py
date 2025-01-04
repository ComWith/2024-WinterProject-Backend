from flask import Flask
from flask_migrate import Migrate
from .models import db  # db 객체 import
from .config import Config  # Config를 사용하여 설정값을 관리합니다.
from .routes import main
import pymysql

# PyMySQL을 MySQLdb 대신 사용하도록 설정
pymysql.install_as_MySQLdb()

# 마이그레이션 인스턴스
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Config 파일에서 설정 불러오기

    # 데이터베이스 URI 설정 (mysql+pymysql://)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://comwith:rootpassward@db/db'

    # db와 migrate 연결
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint 등록
    app.register_blueprint(main)  # Blueprint 등록

    return app
