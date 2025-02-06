import boto3
from app.config import Config
from celery import shared_task

AWS_ACCESS_KEY = Config.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = Config.AWS_SECRET_ACCESS_KEY
AWS_S3_BUCKET_REGION = Config.AWS_S3_BUCKET_REGION
AWS_S3_BUCKET_NAME = Config.AWS_S3_BUCKET_NAME

@shared_task
# s3 bucket에 연결
def s3_connection():
    s3 = boto3.client(
        's3',
        region_name=Config.AWS_S3_BUCKET_REGION,
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )
    return s3

@shared_task
# s3 bucket에 지정 파일 업로드
def s3_put_object(s3, bucket, filepath, access_key):
    try:
        s3.upload_file(
            filepath,
            bucket,
            access_key,
            ExtraArgs={
                'ContentType': 'application/pdf',  # PDF로 인식되도록 설정
                'ContentDisposition': 'inline'  # 브라우저에서 미리보기 가능하게 설정
            }
        )
        print("s3 업로드 완료")
    except Exception as e:
        print(e)
        return False
    return True

@shared_task
# s3 bucket에서 지정 파일 다운로드
def s3_get_object(s3, bucket, object_name, file_name):
    try:
        s3.download_file(bucket, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

