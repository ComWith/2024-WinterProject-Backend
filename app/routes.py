import os
import random
from flask import Blueprint, jsonify, request, abort
from werkzeug.utils import secure_filename
from app.config import Config
from app.klang_api import upload_to_klang
from app.models import db, User, MusicSheet

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return "Hello, Flask!"

# 파일 확장자 체크 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# 파일 저장 함수
def save_file(file):
    try:
        # 업로드 폴더 확인 및 생성
        upload_folder = Config.UPLOAD_FOLDER
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 파일 확장자 검증
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400

        # 파일이 비어 있지 않은지 확인
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            print(f"File saved at: {file_path}")
            return file_path
        else:
            return jsonify({"error": "No file selected or file is empty"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/musicsheets/convert', methods=['POST'])
def convert_music_sheet():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    instrument = request.form.get('instrument')
    title = request.form.get('title')
    composer = request.form.get('composer')
    user_id = request.form.get('user_id')
    stage = request.form.get('stage')

    # 파일이 없으면 오류 반환
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 파일 저장
    file_path = save_file(file)
    if isinstance(file_path, tuple):  # 오류가 발생한 경우
        return file_path

    # Klang API 호출
    try:
        pdf_url = upload_to_klang(file_path, instrument, title, composer)

        # 랜덤 악보 ID 생성 (1부터 1000000 사이의 랜덤 숫자)
        music_sheet_id = random.randint(1, 1000000)

        # MusicSheet 객체 생성 후 DB에 저장
        new_music_sheet = MusicSheet(
            sheet_id=music_sheet_id,
            title=title,
            composer=composer,
            instruments=instrument,
            user_id=user_id,
            stages=stage,
            pdf_url=pdf_url
        )

        db.session.add(new_music_sheet)
        db.session.commit()

        return jsonify({"pdf_url": pdf_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/users/<int:user_id>/musicsheets', methods=['GET'])
def get_all_sheets(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    # 악보 테이블에서 user_id가 일치하는 모든 값을 sheets 리스트에 담기.
    sheets = MusicSheet.query.filter_by(user_id=user_id).all()

    # 변환된 딕셔너리 리스트를 JSON 형식으로 변환후 반환.
    return jsonify([MusicSheet.to_dict_search_all() for MusicSheet in sheets])

@api.route('/musicsheets/<int:sheet_id>', methods=['GET'])
def get_music_sheet(sheet_id):
    sheet_music = MusicSheet.query.get(sheet_id)
    if sheet_music:
        return jsonify(sheet_music.to_dict_search_one()), 200
    return jsonify({"error": "Sheet music not found"}), 404
