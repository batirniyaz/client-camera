from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.working_graphic import create_day, create_working_graphic, \
    get_working_graphics, get_working_graphic, update_working_graphic, delete_working_graphic, get_days, update_day, \
    delete_day
from ..schemas.working_graphic import WorkingGraphicCreate, WorkingGraphicResponse, DayCreate, DayResponse, \
    WorkingGraphicUpdate, DayUpdate
from app.database import get_db

router = APIRouter()


@router.post("/day", response_model=[])
async def create_day_endpoint(day: DayCreate, working_graphic_id: int, db: AsyncSession = Depends(get_db)):
    return await create_day(db, day, working_graphic_id)


@router.post("/", response_model=[])
async def create_working_graphic_endpoint(working_graphic: WorkingGraphicCreate, db: AsyncSession = Depends(get_db)):
    return await create_working_graphic(db, working_graphic)


@router.get("/day/{working_graphic_id}", response_model=list[DayResponse])
async def get_days_endpoint(working_graphic_id: int, db: AsyncSession = Depends(get_db)):
    return await get_days(db, working_graphic_id)


@router.get("/", response_model=list[WorkingGraphicResponse])
async def get_working_graphics_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_working_graphics(db, skip, limit)


@router.get("/{working_graphic_id}", response_model=WorkingGraphicResponse)
async def get_working_graphic_endpoint(working_graphic_id: int, db: AsyncSession = Depends(get_db)):
    return await get_working_graphic(db, working_graphic_id)


@router.put("/{working_graphic_id}", response_model=WorkingGraphicResponse)
async def update_working_graphic_endpoint(working_graphic_id: int, working_graphic: WorkingGraphicUpdate, db: AsyncSession = Depends(get_db)):
    return await update_working_graphic(db, working_graphic_id, working_graphic)


@router.put("/day/{day_id}", response_model=[])
async def update_day_endpoint(day_id: int, day: DayUpdate, db: AsyncSession = Depends(get_db)):
    return await update_day(db, day_id, day)


@router.delete("/{working_graphic_id}")
async def delete_working_graphic_endpoint(working_graphic_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_working_graphic(db, working_graphic_id)


@router.delete("/day/{day_id}")
async def delete_day_endpoint(day_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_day(db, day_id)
