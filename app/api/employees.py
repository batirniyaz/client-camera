import os.path

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ..crud.employee import create_employee, get_employees, store_employee_image, delete_employee, update_employee, get_employee
from ..models import Employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse
from ..schemas.employee_image import EmployeeImageCreate
from ..database import get_db
from ..utils.file_utils import save_upload_file

router = APIRouter()

@router.post("/", response_model=EmployeeResponse)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):

    """
        Create a new employee with the given details.

        - **name**: The name of the employee
        - **phone_number**: The phone number of the employee
        - **position_id**: The ID of the employee's position
        - **filial_id**: The ID of the filial
        - **time_in**: The time the employee checks in
        - **time_out**: The time the employee checks out
        """

    return create_employee(db, employee)


@router.get("/", response_model=List[EmployeeResponse])
def reed_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    """
    Get a list of employees with the given details.
    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return get_employees(db, skip, limit)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):

    """
    Get an employee with the given ID.
    :param employee_id:
    :param db:
    :return:
    """
    return get_employee(db, employee_id)


# @router.post("/images", response_model=EmployeeImageResponse)
# def create_employee_image_endpoint(employee_image: EmployeeImageCreate, db: Session = Depends(get_db)):
#     return create_employee_image(db, employee_image)


@router.post("/{employee_id}/images")
def store_employee_image_endpoint(
        employee_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    """
    Store an image for the employee with the given ID.
    :param employee_id:
    :param file:
    :param db:
    :return:
    """
    main_image_url = f"/storage/users/"
    if not os.path.exists(f"{main_image_url}{employee_id}"):
        os.makedirs(f"{main_image_url}{employee_id}")

    file_path = save_upload_file(file)
    image_url = f"{main_image_url}{employee_id}/images/{file_path}"
    return store_employee_image(db, employee_id, image_url)


@router.delete("/{employee_id}")
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):

    """
    Delete an employee with the given ID.
    :param employee_id:
    :param db:
    :return:
    """
    return delete_employee(db, employee_id)

@router.put("/{employee_id}")
def update_employee_endpoint(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):

    """
    Update an employee with the given ID.
    :param employee_id:
    :param employee:
    :param db:
    :return:
    """
    return update_employee(db, employee_id, employee)
