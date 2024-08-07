from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..crud.position import create_position, get_positions, delete_position, update_position, get_position
from ..schemas.position import PositionCreate, PositionResponse, PositionUpdate
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=PositionResponse)
async def create_position_endpoint(position: PositionCreate, db: AsyncSession = Depends(get_db)):

    """
        Create a new position with the given details.

        - **name**: The name of the position
        """
    return await create_position(db, position)


@router.get("/", response_model=List[PositionResponse])
async def get_positions_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):

    """
    Get a list of positions with the given details.
    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return await get_positions(db, skip, limit)


@router.get("/{position_id}", response_model=PositionResponse)
async def get_position_endpoint(position_id: int, db: AsyncSession = Depends(get_db)):

    """
    Get a position with the given ID.
    :param position_id:
    :param db:
    :return:
    """
    return await get_position(db, position_id)


@router.put("/{position_id}", response_model=PositionResponse)
async def update_position_endpoint(position_id: int, position: PositionUpdate, db: AsyncSession = Depends(get_db)):

    """
    Update a position with the given ID.
    :param position_id:
    :param position:
    :param db:
    """
    return await update_position(db, position_id, position)


@router.delete("/{position_id}")
async def delete_position_endpoint(position_id: int, db: AsyncSession = Depends(get_db)):

    """
    Delete a position with the given ID.
    :param position_id:
    :param db:
    """
    return await delete_position(db, position_id)
