from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..crud.working_graphic import create_working_graphic, get_working_graphics, delete_working_graphic, update_working_graphic, get_working_graphic
from ..schemas.working_graphic import WorkingGraphicCreate, WorkingGraphicResponse, WorkingGraphicUpdate
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=WorkingGraphicResponse)
async def create_working_graphic_endpoint(working_graphic: WorkingGraphicCreate, db: AsyncSession = Depends(get_db)):

    """
        Create a new working graphic with the given details.

        - **start_time**: The start time of the working graphic
        - **end_time**: The end time of the working graphic
        - **employee_id**: The ID of the employee
        """
    return await create_working_graphic(db, working_graphic)


@router.get("/", response_model=List[WorkingGraphicResponse])
async def get_working_graphics_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):

    """
    Get a list of working graphics with the given details.
    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return await get_working_graphics(db, skip, limit)


@router.get("/{working_graphic_id}", response_model=WorkingGraphicResponse)
async def get_working_graphic_endpoint(working_graphic_id: int, db: AsyncSession = Depends(get_db)):

    """
    Get a working graphic with the given ID.
    :param working_graphic_id:
    :param db:
    :return:
    """
    return await get_working_graphic(db, working_graphic_id)


@router.put("/{working_graphic_id}", response_model=WorkingGraphicResponse)
async def update_working_graphic_endpoint(working_graphic_id: int, working_graphic: WorkingGraphicUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a working graphic with the given ID.
    :param working_graphic_id:
    :param working_graphic:
    :param db:
    """
    return await update_working_graphic(db, working_graphic_id, working_graphic)


@router.delete("/{working_graphic_id}")
async def delete_working_graphic_endpoint(working_graphic_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a working graphic with the given ID.
    :param working_graphic_id:
    :param db:
    """

    return await delete_working_graphic(db, working_graphic_id)