import os

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud.employee_image import (
    create_employee_image,
    get_employee_image,
    get_employee_images,
    delete_employee_image,
    update_employee_image,
    )
from ..schemas.employee_image import EmployeeImageCreate, EmployeeImageResponse, EmployeeImageUpdate
from ..database import get_db
from ..utils.file_utils import save_upload_file

router = APIRouter()

@router.post("/", response_model=EmployeeImageResponse)
async def create_employee_image_endpoint(employee_image: EmployeeImageCreate, db: AsyncSession = Depends(get_db)):

    """
    Create a new employee image with the given details.

    - **image_url**: The URL of the image
    - **employee_id**: The ID of the employee
    - **device_id**: The ID of the device
    """

    return await create_employee_image(db, employee_image)


@router.post("/{employee_id}/images")
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
    main_image_url = f"/storage/users/"
    if not os.path.exists(f"{main_image_url}{employee_id}"):
        os.makedirs(f"{main_image_url}{employee_id}")

    file_path = save_upload_file(file)
    image_url = f"{main_image_url}{employee_id}/images/{file_path}"
    return await create_employee_image(db, employee_id, image_url)
