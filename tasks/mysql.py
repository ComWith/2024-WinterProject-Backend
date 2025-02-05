from celery import shared_task
from app.models import db, MusicSheet, Video
from flask import current_app

@shared_task
def save_to_database(pdf_url, sheet_id, title, composer, instrument, user_id, stage):
    from app import create_app  # 순환 참조를 피하기 위해 함수 내부에서 import

    app = current_app._get_current_object() if current_app else create_app()  # 현재 애플리케이션 컨텍스트 사용

    with app.app_context():  # Flask 애플리케이션 컨텍스트 활성화
        try:
            # MusicSheet 객체 생성
            new_music_sheet = MusicSheet(
                sheet_id=sheet_id,
                title=title,
                composer=composer,
                instruments=instrument,
                user_id=user_id,
                stages=stage,
                pdf_url=pdf_url
            )

            # 데이터베이스에 저장
            db.session.add(new_music_sheet)
            db.session.commit()
            return {"status": "success", "pdf_id": pdf_url}

        except Exception as e:
            # 예외 발생 시 롤백
            db.session.rollback()
            raise Exception(f"Database save failed: {str(e)}")

@shared_task
def video_to_database(video_path, video_id, user_id, sheet_id):
    from app import create_app  # 순환 참조를 피하기 위해 함수 내부에서 import

    app = current_app._get_current_object() if current_app else create_app()  # 현재 애플리케이션 컨텍스트 사용

    with app.app_context():  # Flask 애플리케이션 컨텍스트 활성화
        try:
            # Video 객체 생성
            new_video = Video(
                video_id=video_id,
                sheet_id=sheet_id,
                user_id=user_id,
                video_path=video_path
            )

            # 데이터베이스에 저장
            db.session.add(new_video)
            db.session.commit()
            return {"status": "success", "video_path": video_path}

        except Exception as e:
            # 예외 발생 시 롤백
            db.session.rollback()
            raise Exception(f"Database save failed: {str(e)}")