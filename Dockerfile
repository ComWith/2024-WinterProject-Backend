FROM python:3.8

# Flask 앱 환경 구성
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Flask 앱 코드 복사
COPY . app/
# run.py 파일 복사 (최상위 디렉토리에서 복사)
COPY . run.py

EXPOSE 5000

# Flask 실행
CMD ["flask", "run", "--host=0.0.0.0"]