# Python 베이스 이미지 선택
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# MuseScore 설치를 위한 필수 패키지 설치
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    xauth \
    xvfb \
    libgl1-mesa-glx \
    libpulse0 \
    libqt5widgets5 \
    software-properties-common || { echo 'Package installation failed' && exit 1; } \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# MuseScore 설치
RUN apt-get update && apt-get install -y \
    musescore3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 종속성 복사 및 설치
COPY musescore/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt || { echo 'Pip installation failed' && exit 1; }

# 환경변수 설정
ENV QT_QPA_PLATFORM=offscreen

# 애플리케이션 코드 복사
COPY musescore/server.py /app/
COPY musescore/musescore.py /app/

# 포트 노출
EXPOSE 8000

# FastAPI 앱 실행
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
