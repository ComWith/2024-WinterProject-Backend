import logging
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
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


@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    if not (file.filename.lower().endswith(".musicxml") or file.filename.lower().endswith(".xml")):
        raise HTTPException(status_code=400, detail="Only .musicxml or .xml files are supported.")

    input_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    try:
        # 변환된 PDF 경로 확인
        output_pdf_path = convert_musicxml_to_pdf(input_path)

        # 파일 경로가 존재하는지 확인
        if not os.path.exists(output_pdf_path):
            logger.error(f"PDF file not found at: {output_pdf_path}")
            raise HTTPException(status_code=500, detail=f"PDF file not found: {output_pdf_path}")

        # 변환된 PDF 반환
        return FileResponse(output_pdf_path, media_type="application/pdf", filename=os.path.basename(output_pdf_path))
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
    finally:
        # 임시 파일 삭제
        if os.path.exists(input_path):
            os.remove(input_path)
