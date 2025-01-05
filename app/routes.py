from flask import Blueprint
from app.models import User, MusicSheet
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, Flask!"

@main.route('/users/<int:user_id>/musicsheets', methods=['GET'])
def get_all_sheets(user_id):
    user = User.query.get(user_id) # db에서 user_id 찾아오기
    if not user: # db에 없을 시 None 반환
        abort(404, description="User not found")

    # 악보 테이블에서 user_id가 일치하는 모든 값을 sheets 리스트에 담기.
    sheets = MusicSheet.query.filter_by(user_id=user_id).all()

    # 변환된 딕셔너리 리스트를 JSON 형식으로 변환후 반환.
    return jsonify([MusicSheet.to_dict_search_all() for MusicSheet in sheets])


@main.route('/musicsheets/<int:sheet_id>', methods=['GET'])
def get_music_sheet(sheet_id):
    sheet_music = MusicSheet.query.get(sheet_id)
    if sheet_music:
        return jsonify(sheet_music.to_dict_search_one()), 200
    return jsonify({"error": "Sheet music not found"}), 404
