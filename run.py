from app import create_app
import logging
from flask import Flask, request
from flask_cors import CORS

app = create_app()

# 로깅 설정
logging.basicConfig(filename='flask.log', level=logging.INFO)

# CORS 설정 (모든 API에 적용)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


@app.before_request
def log_request_info():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    app.logger.info(f"Request made from IP: {client_ip} to {request.url} with method {request.method}")

@app.after_request
def after_request(response):
    # CORS 설정
    if request.method == "OPTIONS":
        app.logger.info(f"CORS Preflight OPTIONS request received from {request.origin}")

    # CORS 헤더 추가
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')  # 쿠키나 자격증명을 허용

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
