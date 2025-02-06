import requests
import time
from flask import jsonify
import xml.etree.ElementTree as ET
from tasks.stage import *
from tasks.s3 import *

@shared_task(ignore_result=False)
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

        # 실제 요청 보내기
        try:
            response = requests.post(
                f'{API_URL}/transcription',  # API 엔드포인트
                headers={'kl-api-key': API_KEY},
                params=query_parameters,  # URL 쿼리 파라미터
                data=data,  # 폼 데이터
                files=files  # 멀티파트 파일 전송
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()

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

@shared_task(ignore_result=False)
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
        # 바이너리 데이터를 직접 처리하는 방법
        try:
            musicxml_object = io.BytesIO(response.content)
            tree = ET.ElementTree(ET.fromstring(response.content))  # 바이너리 데이터를 XML로 파싱
            root = tree.getroot()

            # 제목과 작곡자 추출
            title = root.find(".//movement-title").text
            composer = root.find(".//identification//creator").text

            print(f"1. Movement Title: {title}")
            print(f"1. Composer: {composer}")
        except Exception as e:
            print(f"Error parsing XML: {e}")
        # 메타데이터 설정 후 반환
        return musicxml_object
    else:
        raise Exception("MusicXML 파일 다운로드 실패")