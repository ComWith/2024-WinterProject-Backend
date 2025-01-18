from flask import Flask
from flask_migrate import Migrate
from .models import db
from .config import Config
from .routes import api
import pymysql
from .redis import get_redis_client
from celery_worker import make_celery

# Redis 클라이언트 생성
redis_client = get_redis_client()

# PyMySQL을 MySQLdb 대신 사용하도록 설정
pymysql.install_as_MySQLdb()

# 마이그레이션 인스턴스
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)  # Config 파일에서 설정 불러오기

    # db와 migrate 연결
    db.init_app(app)
    migrate.init_app(app, db)

    # celery와 flask 연동
    celery = make_celery(app)

    # Blueprint 등록
    app.register_blueprint(api)  # Blueprint 등록

    return app
