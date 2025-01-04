# Python 3.8 이미지를 기반으로 Flask 앱을 빌드
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt # 의존성 설치시 캐시를 사용하지 않도록 설정

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 5000

# Flask 앱 실행
CMD ["python", "run.py"]