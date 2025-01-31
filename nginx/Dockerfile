# 최신 Nginx 이미지 사용
FROM nginx:latest

# Certbot 및 Nginx 플러그인 설치
RUN apt update && apt install -y certbot python3-certbot-nginx

# 기본 설정 파일 삭제 (오타 수정됨)
RUN rm /etc/nginx/conf.d/default.conf

# Nginx 설정 파일 복사 (오타 수정됨)
COPY nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

# Certbot 인증을 위한 폴더 생성
RUN mkdir -p /var/www/certbot

# 80 포트 오픈 (SSL 인증 후 443 오픈 예정)
EXPOSE 80

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]
