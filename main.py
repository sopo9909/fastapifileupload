from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
import uvicorn

app = FastAPI()

# 파일을 저장할 디렉토리 설정
UPLOAD_DIRECTORY = "/mnt/file"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)


@app.post("/upload-zip/")
async def upload_zip_file(file: UploadFile = File(...)):
    # 파일 타입 검증
    if file.content_type != "application/zip":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only zip files are accepted."
        )
    try:
        # 파일 경로 생성
        file_location: str = f"{UPLOAD_DIRECTORY}/{file.filename}"

        # 파일을 임시 파일로 저장
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully.",
                "filename": file.filename,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "An error occurred during file upload.",
                "detail": str(e),
            },
        )


if __name__ == "__main__":
    config: dict = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": 8080,
        "access_log": True,
        "reload": False,
    }
    uvicorn.run(**config)
