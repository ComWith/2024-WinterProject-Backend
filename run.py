from app import create_app
import logging
from flask import Flask, request
from flask_cors import CORS

app = create_app()

# 로깅 설정
logging.basicConfig(filename='flask.log', level=logging.INFO)

# CORS 설정
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def log_request_info():
    app.logger.info(f"Request made to {request.url} with method {request.method}")

@app.after_request
def after_request(response):
    if request.method == "OPTIONS":
        app.logger.info(f"CORS Preflight OPTIONS request received from {request.origin}")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
