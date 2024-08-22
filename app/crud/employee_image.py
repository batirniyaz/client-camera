import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.employee_image import EmployeeImage
from ..schemas.employee_image import EmployeeImageCreate, EmployeeImageUpdate
from ..utils.file_utils import save_upload_file

from ..database import BASE_URL


async def create_employee_image(db: AsyncSession, employee_id: int, file: UploadFile):
    try:
        main_image_url = f"/storage/users/"
        dir_path = f"{main_image_url}{employee_id}"
        img_type = "images"

        if not os.path.exists(dir_path):
            os.makedirs(f"{dir_path}/{img_type}")

        file_path = save_upload_file(file, employee_id, img_type)
        image_url = f"{main_image_url}{employee_id}/{img_type}/{file_path}"

        db_employee_image = EmployeeImage(image_url=image_url, employee_id=employee_id)
        db.add(db_employee_image)
        await db.commit()
        await db.refresh(db_employee_image)

        db_employee_image.image_url = f"{BASE_URL}{image_url}"

        return db_employee_image

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_employees_images(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(EmployeeImage).offset(skip).limit(limit))
    employee_images = result.scalars().all()

    for image in employee_images:
        image.image_url = f"{BASE_URL}{image.image_url}"

    return employee_images


async def get_employee_images(db: AsyncSession, employee_id: int):
    result = await db.execute(select(EmployeeImage).filter_by(employee_id=employee_id))
    employee_images = result.scalars().all()
    if not employee_images:
        raise HTTPException(status_code=404, detail="Employee images not found")

    for image in employee_images:
        image.image_url = f"{BASE_URL}{image.image_url}"

    return employee_images


async def get_employee_image(db: AsyncSession, employee_id: int, employee_image_id: int):
    result = await db.execute(select(EmployeeImage).filter_by(image_id=employee_image_id, employee_id=employee_id))
    employee_image = result.scalar_one_or_none()
    if not employee_image:
        raise HTTPException(status_code=404, detail="Employee image not found")



    return employee_image


async def update_employee_image(db: AsyncSession, employee_id: int, employee_image_id: int, employee_image: EmployeeImageUpdate):
    db_employee_image = await get_employee_image(db, employee_id, employee_image_id)
    for key, value in employee_image.model_dump(exclude_unset=True).items():
        setattr(db_employee_image, key, value)
    await db.commit()
    await db.refresh(db_employee_image)
    return db_employee_image


async def delete_employee_image(db: AsyncSession, employee_id: int, employee_image_id: int):
    db_employee_image = await get_employee_image(db, employee_id, employee_image_id)
    await db.delete(db_employee_image)
    await db.commit()
    return {"message": f"Employee image {employee_image_id} deleted"}
