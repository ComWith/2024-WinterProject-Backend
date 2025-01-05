from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)  # 기본 키로 설정
    name = db.Column(db.String(100), nullable=False)  # 이름
    password = db.Column(db.String(100), nullable=False)  # 비밀번호

class MusicSheet(db.Model):
    __tablename__ = 'musicsheets'

    sheet_id = db.Column(db.String(10), primary_key=True)  # 기본 키로 설정
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 외래 키
    pdf_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    composer = db.Column(db.String(20), nullable=False)
    instruments = db.Column(db.String(20), nullable=False)
    stages = db.Column(db.String(20), nullable=False)

    # 관계 설정
    user = db.relationship('User', backref='musicsheets', lazy=True)

    def to_dict(self):
        return {
            "title": self.title,
            "sheet_id": self.sheet_id
        }