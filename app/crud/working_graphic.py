from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.working_graphic import WorkingGraphic, Day
from ..schemas.working_graphic import WorkingGraphicCreate, WorkingGraphicUpdate, DayCreate, DayUpdate, \
    WorkingGraphicResponse, DayResponse


async def create_day(db: AsyncSession, day: DayCreate, working_graphic_id: int):
    try:
        db_day = Day(**day.model_dump(), working_graphic_id=working_graphic_id)
        db.add(db_day)
        await db.commit()
        await db.refresh(db_day)

    except Exception as e:
        await db.rollback()
        raise e

    return db_day


async def create_working_graphic(db: AsyncSession, working_graphic: WorkingGraphicCreate):
    try:
        db_working_graphic = WorkingGraphic(**working_graphic.model_dump())
        db.add(db_working_graphic)
        await db.commit()
        await db.refresh(db_working_graphic)

    except Exception as e:
        await db.rollback()
        raise e

    return db_working_graphic


async def get_days(db: AsyncSession, working_graphic_id: int):
    result = await db.execute(select(Day).filter_by(working_graphic_id=working_graphic_id))
    return result.scalars().all()

async def get_working_graphics(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(WorkingGraphic).offset(skip).limit(limit))
    working_graphics = result.scalars().all()

    formatted_working_graphics = []
    for working_graphic in working_graphics:
        days_result = await db.execute(select(Day).filter_by(working_graphic_id=working_graphic.id))
        days = days_result.scalars().all()

        formatted_working_graphic = WorkingGraphicResponse(
            id=working_graphic.id,
            name=working_graphic.name,
            days=[
                DayResponse(
                    id=day.id,
                    day=day.day,
                    time_in=day.time_in,
                    time_out=day.time_out,
                    is_work_day=day.is_work_day,
                    created_at=day.created_at,
                    updated_at=day.updated_at,
                ) for day in days
            ],
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
                } for employee in working_graphic.employees
            ],
            created_at=working_graphic.created_at,
            updated_at=working_graphic.updated_at,
        )
        formatted_working_graphics.append(formatted_working_graphic)

    return formatted_working_graphics


async def get_working_graphic(db: AsyncSession, working_graphic_id: int):
    result = await db.execute(select(WorkingGraphic).filter_by(id=working_graphic_id))
    working_graphic = result.scalar_one_or_none()
    if not working_graphic:
        raise Exception("Working graphic not found")

    days_result = await db.execute(select(Day).filter_by(working_graphic_id=working_graphic.id))
    days = days_result.scalars().all()

    formatted_working_graphic = WorkingGraphicResponse(
        id=working_graphic.id,
        name=working_graphic.name,
        days=[
            DayResponse(
                id=day.id,
                day=day.day,
                time_in=day.time_in,
                time_out=day.time_out,
                is_work_day=day.is_work_day,
                created_at=day.created_at,
                updated_at=day.updated_at,
            ) for day in days
        ],
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
            } for employee in working_graphic.employees
        ],
        created_at=working_graphic.created_at,
        updated_at=working_graphic.updated_at,
    )
    return formatted_working_graphic


async def update_working_graphic(db: AsyncSession, working_graphic_id: int, working_graphic: WorkingGraphicUpdate):
    result = await db.execute(select(WorkingGraphic).filter_by(id=working_graphic_id))
    db_working_graphic = result.scalar_one_or_none()

    if not db_working_graphic:
        raise HTTPException(status_code=404, detail="Working graphic not found")

    for key, value in working_graphic.model_dump(exclude_unset=True).items():
        setattr(db_working_graphic, key, value)

    for day in db_working_graphic.days:
        day.working_graphic_id = working_graphic_id

    await db.commit()
    await db.refresh(db_working_graphic)
    return db_working_graphic


async def delete_working_graphic(db: AsyncSession, working_graphic_id: int):
    result = await db.execute(select(WorkingGraphic).filter_by(id=working_graphic_id))
    db_working_graphic = result.scalar_one_or_none()

    if not db_working_graphic:
        raise HTTPException(status_code=404, detail="Working graphic not found")

    for day in db_working_graphic.days:
        await db.delete(day)

    await db.delete(db_working_graphic)
    await db.commit()
    return {"message": f"Working graphic {working_graphic_id} deleted"}
