import logging
from app import create_app
from flask import Flask, request
from flask_cors import CORS

app = create_app()

# 콘솔에 로그 출력
logging.basicConfig(level=logging.INFO)

# CORS 설정 (모든 API에 적용)
CORS(app, resources={r"/*": {
    "origins": "http://localhost:3000",  # 허용할 출처
    "methods": ["GET", "POST", "OPTIONS", "DELETE", "PUT"],  # 허용할 메서드들
    "allow_headers": ["Content-Type", "Authorization"],  # 허용할 헤더들
}}, supports_credentials=True)  # 자격 증명 허용

@app.before_request
def log_request_info():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    app.logger.info(f"Request made from IP: {client_ip} to {request.url} with method {request.method}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
