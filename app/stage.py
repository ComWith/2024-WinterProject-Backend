import requests
import os
import time
from music21 import converter, stream, note, chord, environment, tie
from flask import jsonify
from app.config import Config


def download_xml(xml_url, job_id):
    # API 키 가져오기
    API_KEY = Config.EXTERNAL_API_KEY

    # 작업 상태 URL
    status_url = f"https://api.klang.io/job/{job_id}/status"

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
                time.sleep(10)  # 작업이 진행 중인 경우 10초 대기
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


def convert_musicxml_to_pdf(input_path, level):
    # music21 환경 설정 업데이트
    env = environment.Environment()
    env['musescoreDirectPNGPath'] = '/usr/bin/musescore'  # MuseScore 실행 파일의 정확한 경로
    env['musicxmlPath'] = '/usr/bin/musescore'

    # musicxml 파일 로드
    score = converter.parse(input_path)

    # 난이도 조정
    adjusted_score = adjust_difficulty(score, level)

    # 파일 이름 설정
    filename = os.path.basename(input_path)
    root_name = os.path.splitext(filename)[0]
    temp_xml_path = f"{root_name}.xml"
    adjusted_xml_path = f"{root_name}_adjusted.musicxml"
    output_pdf_path = f"{root_name}_adjusted.pdf"

    # MusicXML 파일로 일시적 저장 (저장할 필요가 있다면)
    adjusted_score.write('musicxml', fp=adjusted_xml_path)

    # PDF로 변환
    adjusted_score.write('musicxml.pdf', fp=output_pdf_path)

    # 임시 파일 삭제
    if os.path.exists(temp_xml_path):
        os.remove(temp_xml_path)
    if os.path.exists(adjusted_xml_path):
        os.remove(adjusted_xml_path)

    return output_pdf_path


def adjust_difficulty(score, level):

    if level == 'easy':
        # 기본 멜로디: 단순한 음표만 유지
        basic_stream = stream.Stream()
        for n in score.flat.notes:
            if isinstance(n, note.Note):
                basic_stream.append(n)
        return basic_stream

    elif level == 'intermediate':
        # 중급: 멜로디에 화음 추가
        intermediate_stream = stream.Stream()
        for n in score.flat.notes:
            if isinstance(n, note.Note):
                c = chord.Chord([n.pitch, n.pitch.transpose(4), n.pitch.transpose(7)])
                c.quarterLength = n.quarterLength
                intermediate_stream.append(c)
        return intermediate_stream

    elif level == 'hard':
        # 고급: 장식음, 리듬 복잡성 및 화음 추가
        advanced_stream = stream.Stream()
        previous_chord = None
        for idx, n in enumerate(score.flat.notes):
            if isinstance(n, note.Note):
                # 화음을 생성하여 각 음표에 추가
                # 기본 음표에 대한 트라이어드 화음을 생성합니다 (예: C-E-G)
                harmony_notes = [n.pitch, n.pitch.transpose(4), n.pitch.transpose(7)]
                new_chord = chord.Chord(harmony_notes)
                new_chord.lyrics.append(note.Lyric("Tr"))

                # 리듬 복잡성 증가를 위한 길이 변경
                if idx % 2 == 0:
                    new_chord.duration.quarterLength = 0.25
                else:
                    new_chord.duration.quarterLength = 0.75

                # 점음표 추가 및 tie 사용
                if previous_chord and idx % 3 == 0:
                    new_chord.duration.quarterLength += 0.5
                    new_chord.tie = tie.Tie('start')
                    previous_chord.tie = tie.Tie('stop')

                advanced_stream.append(new_chord)
                previous_chord = new_chord
        return advanced_stream

    else:
        raise ValueError("Invalid difficulty level specified.")