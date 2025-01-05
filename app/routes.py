from flask import Blueprint, jsonify
from app.models import MusicSheet

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, Flask!"

@main.route('/musicsheets/<int:sheet_id>', methods=['GET'])
def get_music_sheet(sheet_id):
    """
    ID로 특정 악보를 조회합니다.
    """
    sheet_music = MusicSheet.query.get(sheet_id)
    if sheet_music:
        return jsonify(sheet_music.to_dict()), 200
    return jsonify({"error": "Sheet music not found"}), 404