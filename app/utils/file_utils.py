import os
from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IMAGE_DIR = BASE_DIR / "storage" / "users"


def save_upload_file(upload_file: UploadFile) -> str:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    file_location = IMAGE_DIR / upload_file.filename
    with open(file_location, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return upload_file.filename
