import boto3
from app.config import Config

AWS_ACCESS_KEY = Config.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = Config.AWS_SECRET_ACCESS_KEY
AWS_S3_BUCKET_REGION = Config.AWS_S3_BUCKET_REGION
AWS_S3_BUCKET_NAME = Config.AWS_S3_BUCKET_NAME

# s3 bucket에 연결
def s3_connection():
    try:
        s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        print(e)
        exit(ERROR_S3_CONNECTION_FAILED)
    else:
        print("s3 bucket connected!")
        return s3 # s3에 연결된 객체 반환

# s3 bucket에 지정 파일 업로드
def s3_put_object(s3, bucket, filepath, access_key):
    try:
        s3.upload_file(filepath, bucket, access_key)
        print("s3 업로드 완료")
    except Exception as e:
        print(e)
        return False
    return True

# s3 bucket에서 지정 파일 다운로드
def s3_get_object(s3, bucket, object_name, file_name):
    try:
        s3.download_file(bucket, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

