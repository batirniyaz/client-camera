import os
from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IMAGE_DIR = BASE_DIR / "storage" / "users"


def save_upload_file(upload_file: UploadFile, employee_id: int) -> str:
    employee_dir = IMAGE_DIR / str(employee_id) / "images"
    employee_dir.mkdir(parents=True, exist_ok=True)
    file_location = employee_dir / upload_file.filename
    with open(file_location, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return upload_file.filename
