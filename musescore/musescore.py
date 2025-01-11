import os
from music21 import environment, converter

def convert_musicxml_to_pdf(input_path):
    # MuseScore 경로 설정
    env = environment.Environment()
    env['musescoreDirectPNGPath'] = '/usr/bin/mscore3'
    env['musicxmlPath'] = '/usr/bin/mscore3'

    # MusicXML 파일 로드
    score = converter.parse(input_path)

    # 파일 이름 설정
    filename = os.path.basename(input_path)
    root_name = os.path.splitext(filename)[0]
    adjusted_xml_path = f"{root_name}_adjusted.musicxml"
    output_pdf_path = f"{root_name}_adjusted.pdf"

    # MusicXML 파일로 저장
    score.write('musicxml', fp=adjusted_xml_path)

    # PDF로 변환
    score.write('musicxml.pdf', fp=output_pdf_path)

    # 임시 파일 삭제
    if os.path.exists(adjusted_xml_path):
        os.remove(adjusted_xml_path)

    return output_pdf_path
