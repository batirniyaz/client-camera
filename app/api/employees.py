from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..crud.employee import create_employee, get_employees, store_employee_image
from ..schemas.employee import EmployeeCreate, EmployeeResponse
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=EmployeeResponse)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)


@router.get("/", response_model=List[EmployeeResponse])
def reed_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_employees(db, skip, limit)


@router.post("/{employee_id}/images")
def store_employee_image_endpoint(employee_id: int, image_url: str, db: Session = Depends(get_db)):
    return store_employee_image(db, employee_id, image_url)
