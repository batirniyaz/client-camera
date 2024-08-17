from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.working_graphic import WorkingGraphic, Day
from ..schemas.working_graphic import WorkingGraphicCreate, WorkingGraphicUpdate, DayCreate, DayUpdate


async def create_working_graphic(db: AsyncSession, working_graphic: WorkingGraphicCreate):
    try:
        db_working_graphic = WorkingGraphic(**working_graphic.model_dump())
        db.add(db_working_graphic)
        await db.commit()
        await db.refresh(db_working_graphic)

        for day in working_graphic.days:
            db_day = Day(**day.model_dump(), working_graphic_id=db_working_graphic.id)
            db.add(db_day)

        await db.commit()

        return db_working_graphic
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_working_graphics(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(WorkingGraphic).offset(skip).limit(limit))
    return result.scalars().all()


async def get_working_graphic(db: AsyncSession, working_graphic_id: int):
    result = await db.execute(select(WorkingGraphic).filter_by(id=working_graphic_id))
    working_graphic = result.scalar_one_or_none()
    if not working_graphic:
        raise HTTPException(status_code=404, detail="Working graphic not found")
    return working_graphic


async def update_working_graphic(db: AsyncSession, working_graphic_id: int, working_graphic: WorkingGraphicUpdate):
    db_working_graphic = await get_working_graphic(db, working_graphic_id)
    for key, value in working_graphic.model_dump(exclude_unset=True).items():
        setattr(db_working_graphic, key, value)
    await db.commit()
    await db.refresh(db_working_graphic)
    return db_working_graphic


async def delete_working_graphic(db: AsyncSession, working_graphic_id: int):
    db_working_graphic = await get_working_graphic(db, working_graphic_id)
    await db.delete(db_working_graphic)
    await db.commit()
    return {"message": f"Working graphic {working_graphic_id} deleted"}