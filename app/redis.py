import redis
import jwt
import datetime
import pytz
from app.config import Config

# 한국 표준시(KST) 타임존 객체
KST = pytz.timezone('Asia/Seoul')


# Redis 클라이언트를 초기화하여 반환하는 함수
def get_redis_client():
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=int(Config.REDIS_PORT),  # 포트는 정수로 변환
        decode_responses=True  # 문자열 데이터를 디코딩
    )


# JWT 생성 함수 (Access Token)
def access_token(user_id):
    expiration = datetime.datetime.now(KST) + datetime.timedelta(seconds=Config.ACCESS_TOKEN_EXPIRES)
    access_token = jwt.encode({'sub': user_id, 'exp': expiration}, Config.SECRET_KEY, algorithm='HS256')
    return access_token


# JWT 생성 함수 (Refresh Token)
def refresh_token(user_id):
    expiration = datetime.datetime.now(KST) + datetime.timedelta(seconds=Config.REFRESH_TOKEN_EXPIRES)
    refresh_token = jwt.encode({'sub': user_id, 'exp': expiration}, Config.SECRET_KEY, algorithm='HS256')

    # Redis에 리프레시 토큰 저장
    redis_client = get_redis_client()

    # datetime 객체를 timestamp로 변환하여 저장
    expiration_timestamp = int(expiration.timestamp())  # timestamp()는 초 단위로 변환

    # setex 명령을 통해 토큰 만료 시점(expiration_timestamp)에 맞게 자동 삭제되도록 설정
    redis_client.setex(f"user:{user_id}:refresh_token", expiration_timestamp, refresh_token)

    return refresh_token


# Access Token 검증 함수
def verify_access_token(access_token):
    try:
        # 토큰 디코딩
        decoded = jwt.decode(access_token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['sub']

        # 액세스 토큰은 서버에 저장하지 않으므로, 디코딩한 토큰의 유효성만 확인
        return user_id  # 유효한 액세스 토큰일 경우 사용자 ID 반환
    except jwt.ExpiredSignatureError:
        return None  # 만료된 액세스 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 액세스 토큰


# Refresh Token 검증 함수
def verify_refresh_token(refresh_token):
    try:
        # 토큰 디코딩
        decoded = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['sub']

        # Redis에서 해당 사용자 ID에 맞는 리프레시 토큰을 확인
        redis_client = get_redis_client()
        stored_token = redis_client.get(f"user:{user_id}:refresh_token")

        if stored_token and stored_token == refresh_token:
            return user_id  # 토큰 유효하면 사용자 ID 반환
        else:
            return None  # Redis에 없는 토큰이나 일치하지 않으면 None 반환
    except jwt.ExpiredSignatureError:
        return None  # 만료된 리프레시 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 리프레시 토큰


# 리프레시 토큰 삭제 함수
def delete_refresh_token(user_id):
    redis_client = get_redis_client()
    redis_client.delete(f"user:{user_id}:refresh_token")
