import os.path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud.employee import create_employee, get_employees, store_employee_image, del_employee
from ..models import Employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse
from ..database import get_db
from ..utils.file_utils import save_upload_file

router = APIRouter()

UPLOAD_DIRECTORY = "app/uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@router.post("/", response_model=EmployeeResponse)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)


@router.get("/", response_model=List[EmployeeResponse])
def reed_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_employees(db, skip, limit)


@router.post("/{employee_id}/images")
def store_employee_image_endpoint(employee_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = save_upload_file(file)
    image_url = f"/static/images/{file_path}"
    return store_employee_image(db, employee_id, image_url)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    return del_employee(db, employee_id)
