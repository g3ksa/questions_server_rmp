from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os

app = FastAPI()

upload_dir = "uploads"

os.makedirs(upload_dir, exist_ok=True)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    try:
        # Сохраняем файл в директории upload_dir с именем, заданным пользователем
        with open(os.path.join(upload_dir, file.filename), "wb") as f:
            shutil.copyfileobj(file.file, f)
        return JSONResponse(content={"message": "Файл успешно загружен"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(upload_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return JSONResponse(content={"message": "Файл не найден"}, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
