import io
from app.config import Config
from tasks.s3 import s3_connection
from celery import shared_task
from tasks.mysql import video_to_database

AWS_S3_BUCKET_NAME = Config.AWS_S3_BUCKET_NAME

@shared_task
def save_video(file_path, video_id, user_id, sheet_id, video_name):
    s3 = s3_connection()

    # 파일을 바이트 스트림으로 읽기
    with open(file_path, 'rb') as file_data:
        file_stream = io.BytesIO(file_data.read())
        file_stream.seek(0)  # 스트림의 시작으로 포인터를 이동
        # S3 저장
        s3.upload_fileobj(file_stream, AWS_S3_BUCKET_NAME, video_name, ExtraArgs={'ACL': 'public-read'})

    video_path = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{video_name}"

    # MySQL 저장
    video_to_database(video_path, video_id, user_id, sheet_id)

    return {"status": "success", "video_path": video_path}