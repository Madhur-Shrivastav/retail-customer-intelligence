from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import pandas as pd

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1].lower()

    if extension not in ["csv", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if extension == "csv":
        df = pd.read_csv(file_path)

    else:
        df = pd.read_excel(file_path)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns)
    }