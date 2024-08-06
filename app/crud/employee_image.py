from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.employee_image import EmployeeImage
from ..schemas.employee_image import EmployeeImageCreate, EmployeeImageUpdate


async def create_employee_image(db: AsyncSession, employee_image: EmployeeImageCreate):
    try:
        db_employee_image = EmployeeImage(**employee_image.model_dump())
        db.add(db_employee_image)
        await db.commit()
        await db.refresh(db_employee_image)

        return db_employee_image
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_employee_images(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(EmployeeImage).offset(skip).limit(limit))
    return result.scalars().all()


async def get_employee_image(db: AsyncSession, employee_image_id: int):
    result = await db.execute(select(EmployeeImage).filter_by(id=employee_image_id))
    employee_image = result.scalar_one_or_none()
    if not employee_image:
        raise HTTPException(status_code=404, detail="Employee image not found")
    return employee_image


async def update_employee_image(db: AsyncSession, employee_image_id: int, employee_image: EmployeeImageUpdate):
    db_employee_image = await get_employee_image(db, employee_image_id)
    for key, value in employee_image.model_dump(exclude_unset=True).items():
        setattr(db_employee_image, key, value)
    await db.commit()
    await db.refresh(db_employee_image)
    return db_employee_image


async def delete_employee_image(db: AsyncSession, employee_image_id: int):
    db_employee_image = await get_employee_image(db, employee_image_id)
    await db.delete(db_employee_image)
    await db.commit()
    return {"message": f"Employee image {employee_image_id} deleted"}
