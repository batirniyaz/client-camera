from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import Employee
from ..models.filial import Filial
from ..schemas.filial import FilialCreate, FilialUpdate, FilialResponse


async def create_filial(db: AsyncSession, filial: FilialCreate):
    try:
        db_filial = Filial(**filial.model_dump())
        db.add(db_filial)
        await db.commit()
        await db.refresh(db_filial)

        return db_filial
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_filials(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Filial).offset(skip).limit(limit))
    filials = result.scalars().all()

    formatted_filials = []
    for filial in filials:
        employees_result = await db.execute(select(Employee).filter_by(filial_id=filial.id))
        employees = employees_result.scalars().all()

        formatted_filial = FilialResponse(
            id=filial.id,
            name=filial.name,
            address=filial.address,
            employees=[
                {
                    "id": employee.id,
                    "name": employee.name,
                    "phone_number": employee.phone_number,
                    "position_id": employee.position_id,
                    "working_graphic_id": employee.working_graphic_id,
                    "filial_id": employee.filial_id,
                    "created_at": employee.created_at,
                    "updated_at": employee.updated_at,
                } for employee in employees
            ],
            created_at=filial.created_at,
            updated_at=filial.updated_at,
        )
        formatted_filials.append(formatted_filial)

    return formatted_filials


async def get_filial(db: AsyncSession, filial_id: int):
    result = await db.execute(select(Filial).filter_by(id=filial_id))
    filial = result.scalar_one_or_none()
    if not filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    employees_result = await db.execute(select(Employee).filter_by(filial_id=filial.id))
    employees = employees_result.scalars().all()

    formatted_filial = FilialResponse(
        id=filial.id,
        name=filial.name,
        address=filial.address,
        employees=[
            {
                "id": employee.id,
                "name": employee.name,
                "phone_number": employee.phone_number,
                "position_id": employee.position_id,
                "working_graphic_id": employee.working_graphic_id,
                "filial_id": employee.filial_id,
                "created_at": employee.created_at,
                "updated_at": employee.updated_at,
            } for employee in employees
        ],
        created_at=filial.created_at,
        updated_at=filial.updated_at,
    )

    return formatted_filial


async def update_filial(db: AsyncSession, filial_id: int, filial: FilialUpdate):
    db_filial = await get_filial(db, filial_id)
    for key, value in filial.model_dump(exclude_unset=True).items():
        setattr(db_filial, key, value)
    await db.commit()
    await db.refresh(db_filial)
    return db_filial


async def delete_filial(db: AsyncSession, filial_id: int):
    db_filial = await get_filial(db, filial_id)
    await db.delete(db_filial)
    await db.commit()
    return {"message": f"Filial {filial_id} deleted"}
