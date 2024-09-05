from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..database import BASE_URL
from ..models import Employee
from ..models.position import Position
from ..schemas.position import PositionCreate, PositionUpdate, PositionResponse


async def create_position(db: AsyncSession, position: PositionCreate):
    try:
        db_position = Position(**position.model_dump())
        db.add(db_position)
        await db.commit()
        await db.refresh(db_position)

        return db_position
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_positions(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Position).offset(skip).limit(limit))
    positions = result.scalars().all()

    formatted_positions = []
    for position in positions:
        employees = await db.execute(select(Employee).filter_by(position_id=position.id))
        employees = employees.scalars().all()

        formatted_position = PositionResponse(
            id=position.id,
            name=position.name,
            employees=[
                {
                    "id": employee.id,
                    "name": employee.name,
                    "phone_number": employee.phone_number,
                    "position": employee.position.name if employee.position else None,
                    "working_graphic": employee.working_graphic.name if employee.working_graphic else None,
                    "filial": employee.filial.name if employee.filial else None,
                    "images": [
                        {
                            "id": image.image_id,
                            "url": f"{BASE_URL}{image.image_url}"
                        } for image in employee.images
                    ],
                    "created_at": employee.created_at,
                    "updated_at": employee.updated_at,
                } for employee in employees
            ],
            created_at=position.created_at,
            updated_at=position.updated_at,
        )
        formatted_positions.append(formatted_position)

    return formatted_positions


async def get_position(db: AsyncSession, position_id: int):
    result = await db.execute(select(Position).filter_by(id=position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    employees_result = await db.execute(select(Employee).filter_by(position_id=position.id))
    employees = employees_result.scalars().all()

    formatted_position = PositionResponse(
        id=position.id,
        name=position.name,
        employees=[
            {
                "id": employee.id,
                "name": employee.name,
                "phone_number": employee.phone_number,
                "position": employee.position.name if employee.position else None,
                "working_graphic": employee.working_graphic.name if employee.working_graphic else None,
                "filial": employee.filial.name if employee.filial else None,
                "images": [
                    {
                        "id": image.image_id,
                        "url": f"{BASE_URL}{image.image_url}"
                    } for image in employee.images
                ],
                "created_at": employee.created_at,
                "updated_at": employee.updated_at,
            } for employee in employees
        ],
        created_at=position.created_at,
        updated_at=position.updated_at,
    )

    return formatted_position


async def update_position(db: AsyncSession, position_id: int, position: PositionUpdate):
    result = await db.execute(select(Position).filter_by(id=position_id))
    db_position = result.scalar_one_or_none()

    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")

    for key, value in position.model_dump(exclude_unset=True).items():
        setattr(db_position, key, value)
    await db.commit()
    await db.refresh(db_position)
    return db_position


async def delete_position(db: AsyncSession, position_id: int):
    result = await db.execute(select(Position).filter_by(id=position_id))
    db_position = result.scalar_one_or_none()

    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")

    await db.delete(db_position)
    await db.commit()
    return {"message": f"Position {position_id} deleted"}
