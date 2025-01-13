import logging
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse
from musescore import convert_musicxml_to_pdf

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 파일 삭제 함수
def delete_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")

@app.post("/convert")
async def convert_file(background_tasks: BackgroundTasks,
                       file: UploadFile = File(...),
                       title: str = Form(...),
                       composer: str = Form(...)):
    # 파일 확장자 체크
    if not (file.filename.lower().endswith(".musicxml") or file.filename.lower().endswith(".xml")):
        raise HTTPException(status_code=400, detail="Only .musicxml or .xml files are supported.")

    input_path = os.path.join(UPLOAD_DIR, file.filename)

    # 파일 저장
    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    try:
        # MusicXML 파일을 PDF로 변환
        output_pdf_path = convert_musicxml_to_pdf(input_path, title=title, composer=composer)

        if not os.path.exists(output_pdf_path):
            logger.error(f"PDF file not found at: {output_pdf_path}")
            raise HTTPException(status_code=500, detail=f"PDF file not found: {output_pdf_path}")

        # 변환된 PDF 반환
        response = FileResponse(output_pdf_path, media_type="application/pdf", filename=os.path.basename(output_pdf_path))

        # 응답 후에 파일 삭제 작업을 백그라운드에서 수행
        background_tasks.add_task(delete_file, input_path)  # 원본 XML 파일 삭제
        background_tasks.add_task(delete_file, output_pdf_path)  # 변환된 PDF 파일 삭제

        return response

    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
