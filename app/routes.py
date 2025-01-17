import random
from datetime import timedelta
from flask import Blueprint, jsonify, request, abort
from celery_worker.klang_api import upload_to_klang, download_xml
from app.models import db, User, MusicSheet
from app.redis import access_token, refresh_token, verify_refresh_token, verify_access_token, delete_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from celery_worker.stage import *

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return "Hello, Flask!"

# 회원가입
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    nickname = data.get('nickname')

    if not user_id or not password or not nickname:
        return jsonify({"error": "User ID, password, and nickname are required"}), 400

    # 중복 확인
    if User.query.filter_by(user_id=user_id).first() or User.query.filter_by(nickname=nickname).first():
        return jsonify({"error": "User ID or nickname already exists"}), 400

    # 비밀번호 해싱 및 사용자 저장
    hashed_password = generate_password_hash(password)
    new_user = User(user_id=user_id, password=hashed_password, nickname=nickname)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# 로그인
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({"error": "User ID and password are required"}), 400

    # 사용자 인증
    user = User.query.filter_by(user_id=user_id).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # 토큰 생성
    access_token_value = access_token(user_id)
    refresh_token_value = refresh_token(user_id)

    # 응답에 Refresh Token을 HTTP-only 쿠키로 설정
    response = jsonify({
        "message": "Login successful",
        "access_token": access_token_value
    })
    # refresh_token을 HTTP-only 쿠키에 저장
    response.set_cookie('refresh_token', refresh_token_value,
                        httponly=True, secure=False,  # HTTP에서는 secure=False
                        max_age=timedelta(days=30), path='/')

    return response, 200

# 새 Access Token 발급
@api.route('/refresh', methods=['POST'])
def refresh_access_token():
    # 클라이언트에서 Refresh Token을 받아옴
    refresh_token = request.cookies.get('refresh_token')  # 또는 헤더로 전달

    # Refresh Token 검증
    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    # 새 Access Token 생성
    new_access_token = access_token(user_id)

    return jsonify({"access_token": new_access_token}), 200

# 로그아웃
@api.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    refresh_token_value = data.get('refresh_token')

    if not refresh_token_value:
        return jsonify({"error": "Refresh token is required"}), 400

    user_id = verify_refresh_token(refresh_token_value)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Redis에서 Refresh Token 삭제
    delete_refresh_token(user_id)

    # 쿠키에서 refresh_token 삭제
    response = jsonify({"message": "Logout successful"})
    response.delete_cookie('refresh_token', path='/')

    return response, 200

# 악보 변환
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

    # 유효한 난이도 값인지 확인
    valid_levels = ['easy', 'intermediate', 'hard']
    if stage not in valid_levels:
        return jsonify({"error": f"Invalid difficulty level: {stage}. Valid levels are {valid_levels}"}), 400

    # Klang API 호출
    try:
        # MusicSheet 객체 생성 후 DB에 저장
        music_sheet_id = random.randint(1, 1000000)

        # XML URL과 job_id를 받아오는 함수 예시 (실제 구현에 맞게 수정)
        xml_url, job_id = upload_to_klang(file, instrument, title, composer)

        # MusicXML 다운로드
        file_stream = download_xml(xml_url, job_id)

        # 난이도 변환
        difficulty_stream = adjust_difficulty(file_stream, level=stage, title=title, composer=composer)

        # Stream 객체를 MusicXML 파일로 저장, pdf 변환 및 S3 업로드
        pdf_s3_url = stream_to_pdf_and_upload(difficulty_stream, title=title, composer=composer, sheet_id=music_sheet_id)

        new_music_sheet = MusicSheet(
            sheet_id=music_sheet_id,
            title=title,
            composer=composer,
            instruments=instrument,
            user_id=user_id,
            stages=stage,
            pdf_url=pdf_s3_url  # S3 URL 저장
        )

        db.session.add(new_music_sheet)
        db.session.commit()

        return jsonify({"pdf_url": pdf_s3_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 사용자 악보 조회
@api.route('/users/<string:user_id>/musicsheets', methods=['GET'])
def get_all_sheets(user_id):
    # 인증을 위한 액세스 토큰 검증
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    access_token_value = auth_header.split(" ")[1]
    user_id_from_token = verify_access_token(access_token_value)
    if not user_id_from_token:
        return jsonify({"error": "Invalid or expired access token"}), 401

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        abort(404, description="User not found")

    sheets = MusicSheet.query.filter_by(user_id=user_id).all()

    return jsonify([sheet.to_dict_search_all() for sheet in sheets])

# 특정 악보 조회
@api.route('/musicsheets/<int:sheet_id>', methods=['GET'])
def get_music_sheet(sheet_id):
    # 인증을 위한 액세스 토큰 검증
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    access_token_value = auth_header.split(" ")[1]
    user_id_from_token = verify_access_token(access_token_value)
    if not user_id_from_token:
        return jsonify({"error": "Invalid or expired access token"}), 401

    sheet_music = MusicSheet.query.get(sheet_id)
    if sheet_music:
        return jsonify(sheet_music.to_dict_search_one()), 200
    return jsonify({"error": "Sheet music not found"}), 404

# 악보 삭제
@api.route('/musicsheets/<int:sheet_id>', methods=['DELETE'])
def delete_music_sheet(sheet_id):
    # 인증을 위한 액세스 토큰 검증
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    access_token_value = auth_header.split(" ")[1]
    user_id_from_token = verify_access_token(access_token_value)
    if not user_id_from_token:
        return jsonify({"error": "Invalid or expired access token"}), 401

    try:
        sheet_music = MusicSheet.query.get(sheet_id)
        if sheet_music:
            db.session.delete(sheet_music)
            db.session.commit()
            return jsonify({"message": "Deleted successfully"}), 200
        return jsonify({"error": "Music sheet not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during deletion", "details": str(e)}), 500
