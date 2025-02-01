# 최신 Nginx 이미지 사용
FROM nginx:latest

# 기본 설정 파일 삭제 (오타 수정됨)
RUN rm /etc/nginx/conf.d/default.conf

# Nginx 설정 파일 복사 (오타 수정됨)
COPY nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

# 80 포트 오픈 (SSL 인증 후 443 오픈 예정)
EXPOSE 80

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]
