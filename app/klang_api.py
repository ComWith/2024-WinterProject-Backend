import requests
from app.config import Config
import time

def upload_to_klang(file, instrument, title, composer):
    print(f"Received file: {file.filename}, Instrument: {instrument}, Title: {title}, Composer: {composer}")

    # 쿼리 파라미터 설정
    query_parameters = {
        'model': str(instrument),  # 악기 모델
        'title': str(title),  # 제목
        'composer': str(composer),  # 작곡가
    }

    # 파일이 없으면 오류 발생
    if file is None or file.filename == '':
        raise Exception("No file provided")

    try:
        # 멀티파트 파일 전송 파라미터 설정
        files = {
            'file': (file.filename, file.stream, file.content_type)  # 실제 파일의 스트림을 전송
        }
        data = {
            'outputs': 'mxml'
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

        # 실제 요청 보내기
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

                    # job_id 추출 및 MusicXML URL 생성
                    job_id = response_data.get('job_id')
                    if not job_id:
                        raise Exception("Missing 'job_id' in response")

                    xml_url = f'{API_URL}/job/{job_id}/xml'
                    print(f"Generated MusicXML URL: {xml_url}")
                    return xml_url, job_id
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

def download_xml(xml_url, job_id):

    API_KEY = Config.EXTERNAL_API_KEY
    API_URL = Config.EXTERNAL_API_URL

    # 작업 상태 URL
    status_url = f"{API_URL}/job/{job_id}/status"

    # 헤더 구성
    headers = {
        "kl-api-key": API_KEY
    }

    # 작업 완료 여부 확인
    while True:
        status_response = requests.get(status_url, headers=headers)
        if status_response.status_code == 200:
            status_data = status_response.json()
            if status_data.get('status') == 'COMPLETED':
                break  # 작업 완료 시 루프 탈출
            elif status_data.get('status') == 'FAILED':
                return jsonify({"error": "Job failed!"}), 400
            else:
                print("작업 진행 중입니다..")
                time.sleep(15)  # 작업이 진행 중인 경우 10초 대기
        else:
            return print(f"상태 확인 요청 실패: 상태 코드 {status_response.status_code}, 응답: {status_response.text}")

    # 작업 완료 후 MusicXML 다운로드
    response = requests.get(xml_url, headers=headers)
    if response.status_code == 200:
        file_path = f"{job_id}.xml"
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"MusicXML 파일이 성공적으로 다운로드되었습니다: {file_path}")
        return file_path
    else:
        return print(f"MusicXML 파일 요청 실패: 상태 코드 {response.status_code}, 응답: {response.text}")