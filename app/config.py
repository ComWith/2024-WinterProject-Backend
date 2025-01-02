import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False