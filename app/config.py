import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 환경 변수에서 MySQL 연결 정보 읽어오기
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
