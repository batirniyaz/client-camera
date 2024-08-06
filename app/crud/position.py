from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.position import Position
from ..schemas.position import PositionCreate, PositionUpdate


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
    return result.scalars().all()


async def get_position(db: AsyncSession, position_id: int):
    result = await db.execute(select(Position).filter_by(id=position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


async def update_position(db: AsyncSession, position_id: int, position: PositionUpdate):
    db_position = await get_position(db, position_id)
    for key, value in position.model_dump(exclude_unset=True).items():
        setattr(db_position, key, value)
    await db.commit()
    await db.refresh(db_position)
    return db_position


async def delete_position(db: AsyncSession, position_id: int):
    db_position = await get_position(db, position_id)
    await db.delete(db_position)
    await db.commit()
    return {"message": f"Position {position_id} deleted"}
