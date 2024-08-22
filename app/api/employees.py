from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..crud.employee import create_employee, get_employees, delete_employee, update_employee, get_employee, get_employee_deep
from ..schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=[])
async def create_employee_endpoint(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    """
        Create a new employee with the given details.

        - **name**: The name of the employee
        - **phone_number**: The phone number of the employee
        - **position_id**: The ID of the employee's position
        - **filial_id**: The ID of the filial
        """

    return await create_employee(db, employee)


@router.get("/", response_model=List[EmployeeResponse])
async def get_employees_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Get a list of employees with the given details.
    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return await get_employees(db, skip, limit)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get an employee with the given ID.
    :param employee_id:
    :param db:
    :return:
    """
    return await get_employee(db, employee_id)


@router.get("/deep/{employee_id}", response_model=[])
async def get_employee_deep_endpoint(employee_id: int, date: str, db: AsyncSession = Depends(get_db)):
    """
    Get an employee with the given ID.
    :param date:
    :param employee_id:
    :param db:
    :return:
    """
    return await get_employee_deep(db, employee_id, date)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(employee_id: int, employee: EmployeeUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an employee with the given ID.
    :param employee_id:
    :param employee:
    :param db:
    :return:
    """
    return await update_employee(db, employee_id, employee)


@router.delete("/{employee_id}")
async def delete_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an employee with the given ID.
    :param employee_id:
    :param db:
    :return:
    """
    return await delete_employee(db, employee_id)
