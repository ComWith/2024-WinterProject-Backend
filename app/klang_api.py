import os
import requests
from app.config import Config

def upload_to_klang(file_path, instrument, title, composer):
    print(f"Received file: {file_path}, Instrument: {instrument}, Title: {title}, Composer: {composer}")

    # 쿼리 파라미터 설정
    query_parameters = {
        'model': str(instrument),  # 악기 모델
        'title': str(title),  # 제목
        'composer': str(composer),  # 작곡가
    }

    # 파일 경로 확인
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    try:
        with open(file_path, 'rb') as file:
            # 멀티파트 파일 전송 파라미터 설정
            files = {
                'file': file  # 실제 파일
            }
            data = {
                'outputs': 'pdf'  # PDF 요청 (단일 항목으로 전달)
            }

            # 요청 전 파라미터 출력 (디버깅용)
            print(f"Query Parameters: {query_parameters}")
            print(f"Data: {data}")
            print(f"Files: {files}")

            # API 키와 URL 설정
            API_KEY = Config.EXTERNAL_API_KEY
            API_URL = Config.EXTERNAL_API_URL

            print(f"API URL: {API_URL}")
            print(f"API Key: {API_KEY}")

            # 실제 요청 보내기 전에 확인
            try:
                response = requests.post(
                    f'{API_URL}/transcription',  # API 엔드포인트
                    headers={'kl-api-key': API_KEY},
                    params=query_parameters,  # URL 쿼리 파라미터
                    data=data,  # 폼 데이터
                    files=files  # 멀티파트 파일 전송
                )

                # 응답 상태 코드 및 내용 출력
                print(f"API Status Code: {response.status_code}")
                print(f"API Response Text: {response.text}")

                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        print(f"Response JSON: {response_data}")

                        # job_id 추출 및 PDF URL 생성
                        job_id = response_data.get('job_id')
                        if not job_id:
                            raise Exception("Missing 'job_id' in response")

                        pdf_url = f'{API_URL}/job/{job_id}/pdf'
                        print(f"Generated PDF URL: {pdf_url}")
                        return pdf_url
                    except ValueError as json_err:
                        # JSON 형식이 아닌 경우 에러 처리
                        print(f"Failed to parse JSON response: {json_err}")
                        print(f"Response Text: {response.text}")
                        raise Exception("Invalid JSON response")
                else:
                    raise Exception(f"Failed to create job: {response.text}")

            except requests.exceptions.RequestException as req_err:
                print(f"Request failed: {req_err}")
                raise

    except Exception as e:
        print(f"Exception occurred: {e}")
        raise