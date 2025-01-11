import requests
import os
from flask import jsonify
from app.config import Config
from app.s3 import s3_put_object, s3_connection
from music21 import converter, stream, note, chord, tie

FASTAPI_URL = Config.FASTAPI_URL
AWS_S3_BUCKET_NAME = Config.AWS_S3_BUCKET_NAME
AWS_ACCESS_KEY = Config.AWS_ACCESS_KEY
s3 = s3_connection()

# 난이도 변환
def adjust_difficulty(input_path, level):
    score = converter.parse(input_path)  # MusicXML 파일을 `Stream` 객체로 변환

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

# Stream 객체를 MusicXML 파일로 저장하는 함수 추가
def save_stream_as_musicxml(stream_obj, file_path):
    # 주어진 Stream 객체를 MusicXML 파일로 저장
    stream_obj.write("musicxml", fp=file_path)
    return file_path

def convert_musicxml_to_pdf(input_path):
    print("in")
    # MusicXML 파일을 읽어서 FastAPI로 전송
    with open(input_path, "rb") as file:
        files = {"file": (os.path.basename(input_path), file, "application/xml")}
        print("middle")
        response = requests.post(FASTAPI_URL, files=files, timeout=10)
        print("out")

    # 요청 실패 시 에러 처리
    if response.status_code != 200:
        return jsonify({"error": f"Conversion failed: {response.text}"}), 500

    # PDF 파일이 성공적으로 반환되었으면 저장
    pdf_output_path = os.path.splitext(input_path)[0] + ".pdf"
    with open(pdf_output_path, "wb") as pdf_file:
        pdf_file.write(response.content)

    print(f"PDF 파일이 성공적으로 저장되었습니다: {pdf_output_path}")

    # S3로 업로드
    try:
        # 업로드할 파일 경로에서 파일 이름만 추출
        pdf_file_name = os.path.basename(pdf_output_path)

        # 파일 업로드 (ACL을 public-read로 설정)
        s3.upload_file(
            pdf_output_path,
            AWS_S3_BUCKET_NAME,
            pdf_file_name,
            ExtraArgs={'ACL': 'public-read'}
        )

        # S3 URL 생성
        pdf_s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{pdf_file_name}"
        return pdf_s3_url  # PDF 파일의 S3 URL 반환
    except Exception as e:
        print(f"Error uploading PDF to S3: {e}")
        return jsonify({"error": "Failed to upload PDF to S3"}), 500
