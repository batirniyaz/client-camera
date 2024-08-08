import os
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud.employee_image import (
    create_employee_image,
    get_employee_images,
    get_employees_images,
    delete_employee_image,
    update_employee_image,
    get_employee_image,
    )
from ..schemas.employee_image import EmployeeImageResponse, EmployeeImageUpdate
from ..database import get_db

router = APIRouter()


@router.post("/{employee_id}/images", response_model=EmployeeImageResponse)
async def create_employee_image_endpoint(
        employee_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):

    """
    Store an image for the employee with the given ID.
    :param employee_id:
    :param file:
    :param db:
    :return:
    """

    return await create_employee_image(db, employee_id, file)


@router.get("/images", response_model=List[EmployeeImageResponse])
async def get_employees_images_endpoint(db: AsyncSession = Depends(get_db)):

    """
    Get an image for the employee with the given ID.
    :param employee_id:
    :param db:
    :return:
    """
    return await get_employees_images(db)


@router.get("/{employee_id}/images/", response_model=List[EmployeeImageResponse])
async def get_employee_images_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):

    """
    Get an image for the employee with the given ID.
    :param employee_id:
    :param employee_image_id:
    :param db:
    :return:
    """
    return await get_employee_images(db, employee_id)


@router.get("/{employee_id}/images/{employee_image_id}", response_model=EmployeeImageResponse)
async def get_employee_image_endpoint(employee_id: int, employee_image_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get an image for the employee with the given ID.
    :param employee_id:
    :param employee_image_id:
    :param db:
    :return:
    """
    return await get_employee_image(db, employee_id, employee_image_id)


@router.put("/{employee_id}/images/{employee_image_id}", response_model=EmployeeImageResponse)
async def update_employee_image_endpoint(
        employee_id: int,
        employee_image_id: int,
        employee_image: EmployeeImageUpdate,
        db: AsyncSession = Depends(get_db)
):

    """
    Update an image for the employee with the given ID.
    :param employee_id:
    :param employee_image_id:
    :param employee_image:
    :param db:
    :return:
    """
    return await update_employee_image(db, employee_id, employee_image_id, employee_image)


@router.delete("/{employee_id}/images/{employee_image_id}")
async def delete_employee_image_endpoint(employee_id: int, employee_image_id: int, db: AsyncSession = Depends(get_db)):

    """
    Delete an image for the employee with the given ID.
    :param employee_id:
    :param employee_image_id:
    :param db:
    :return:
    """
    return await delete_employee_image(db, employee_id, employee_image_id)
