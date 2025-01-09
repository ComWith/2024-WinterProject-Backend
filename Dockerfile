# Ubuntu 20.04 LTS 이미지를 기반으로 Flask 앱과 MuseScore를 빌드
FROM ubuntu:20.04

# 필수 패키지 및 Python 설치
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.8 \
    python3-pip \
    wget \
    xauth \
    xvfb \
    libgl1-mesa-glx \
    libpulse0 \
    libqt5widgets5 \
    software-properties-common \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# MuseScore PPA 추가 및 설치 시도
RUN add-apt-repository ppa:mscore-ubuntu/mscore-stable \
    && apt-get update \
    && apt-get install -y musescore || apt-get install -y musescore3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 환경변수 설정
ENV QT_QPA_PLATFORM=offscreen

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 먼저 복사하여 캐시 레이어 활용
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 5000

# Flask 앱 실행
CMD ["flask", "run", "--host=0.0.0.0"]
