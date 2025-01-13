import os
from music21 import environment, converter, metadata

def convert_musicxml_to_pdf(input_path, title="Untitled", composer="Unknown Composer"):
    print("start")
    # MuseScore 경로 설정
    env = environment.Environment()
    env['musescoreDirectPNGPath'] = '/usr/bin/mscore3'
    env['musicxmlPath'] = '/usr/bin/mscore3'

    # MusicXML 파일 로드
    score = converter.parse(input_path)

    # 타이틀과 작곡가 설정
    score.metadata = metadata.Metadata()
    score.metadata.title = title
    score.metadata.composer = composer

    # 파일 이름 설정
    filename = os.path.basename(input_path)
    root_name = os.path.splitext(filename)[0]
    adjusted_xml_path = f"{root_name}_adjusted.musicxml"
    output_pdf_path = f"{root_name}_adjusted.pdf"

    # MusicXML 파일로 저장 (타이틀과 작곡가를 포함)
    score.write('musicxml', fp=adjusted_xml_path)

    # PDF로 변환
    score.write('musicxml.pdf', fp=output_pdf_path)

    # 임시 파일 삭제
    if os.path.exists(adjusted_xml_path):
        os.remove(adjusted_xml_path)
    print("finish")
    return output_pdf_path
