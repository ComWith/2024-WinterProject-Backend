import requests
import tempfile
import io
import os
from app.config import Config
from tasks.s3 import s3_connection
from music21 import converter, stream, note, chord, tie
from app.celery_util import celery

FASTAPI_URL = Config.FASTAPI_URL
AWS_S3_BUCKET_NAME = Config.AWS_S3_BUCKET_NAME
AWS_ACCESS_KEY = Config.AWS_ACCESS_KEY
s3 = s3_connection()

@celery.task
# 난이도 변환
def adjust_difficulty(file_path, level, title, composer):
    # 임시 파일 경로를 music21의 converter.parse에 전달
    score = converter.parse(file_path)

    # 작업 완료 된 임시 파일 수동 삭제
    os.remove(file_path)

    # 메타데이터를 직접 설정
    score.metadata.title = title
    score.metadata.composer = composer

    print(f"2. Title: {score.metadata.title}")
    print(f"2. Composer: {score.metadata.composer}")

    if level == 'easy':
        # 기본 멜로디: 단순한 음표만 유지
        processed_stream = stream.Stream()
        for n in score.flat.notes:
            if isinstance(n, note.Note):
                processed_stream.append(n)

    elif level == 'intermediate':
        # 중급: 멜로디에 화음 추가
        processed_stream = stream.Stream()
        for n in score.flat.notes:
            if isinstance(n, note.Note):
                c = chord.Chord([n.pitch, n.pitch.transpose(4), n.pitch.transpose(7)])
                c.quarterLength = n.quarterLength
                processed_stream.append(c)

    elif level == 'hard':
        # 고급: 장식음, 리듬 복잡성 및 화음 추가
        processed_stream = stream.Stream()
        previous_chord = None
        for idx, n in enumerate(score.flat.notes):
            if isinstance(n, note.Note):
                # 화음을 생성하여 각 음표에 추가
                harmony_notes = [n.pitch, n.pitch.transpose(4), n.pitch.transpose(7)]
                new_chord = chord.Chord(harmony_notes)

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

                processed_stream.append(new_chord)
                previous_chord = new_chord

    else:
        raise ValueError("Invalid difficulty level specified.")

    # 결과를 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".musicxml") as temp_file:
        processed_stream.write(fmt="musicxml", fp=temp_file.name)
        result_file_path = temp_file.name

    return result_file_path

@celery.task
def stream_to_pdf_and_upload(file_path, title, composer, sheet_id):
    # 파일 경로로부터 MusicXML 파일을 읽어 FastAPI 서버로 전송
    with open(file_path, "rb") as f:
        files = {'file': ('musicxml.xml', f, 'application/xml')}
        data = {'title': title, 'composer': composer}
        response = requests.post(FASTAPI_URL, files=files, data=data, timeout=10)

    os.remove(file_path)  # 작업 후 임시 파일 삭제

    if response.status_code == 200:
        # 응답으로 받은 PDF 데이터를 S3에 업로드
        pdf_data = response.content  # PDF 데이터가 바이트 형태로 반환됨
        pdf_stream = io.BytesIO(pdf_data)
        file_name = f"{sheet_id}.pdf"

        s3.upload_fileobj(pdf_stream, AWS_S3_BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'})

        # S3 URL 반환
        return f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    else:
        # 에러 메시지와 함께 실패 응답 반환
        error_message = f"Failed to convert PDF with status code {response.status_code}: {response.text}"
        return {"error": error_message}