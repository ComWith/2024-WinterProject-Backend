import random
from flask import Blueprint, jsonify, request, abort
from app.klang_api import upload_to_klang
from app.models import db, User, MusicSheet

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return "Hello, Flask!"

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

    # Klang API 호출
    try:
        pdf_url = upload_to_klang(file, instrument, title, composer)

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


@api.route('/musicsheets/<int:sheet_id>', methods=['DELETE'])
def delete_music_sheet(sheet_id):
    try:
        sheet_music = MusicSheet.query.get(sheet_id)
        if sheet_music:
            db.session.delete(sheet_music)
            db.session.commit()
            return jsonify({"messeage":"Deleted successfully"}), 200
        return jsonify({"error": "Music sheet not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during deletion",
                        "details": str(e)}), 500