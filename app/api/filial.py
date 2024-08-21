from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..crud.filial import create_filial, get_filials, delete_filial, update_filial, get_filial, get_filial_employees_by_date
from ..schemas.filial import FilialCreate, FilialResponse, FilialUpdate
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=FilialResponse)
async def create_filial_endpoint(filial: FilialCreate, db: AsyncSession = Depends(get_db)):

    """
        Create a new filial with the given details.

        - **name**: The name of the filial
        - **address**: The address of the filial
        - **phone_number**: The phone number of the filial
        """
    return await create_filial(db, filial)


@router.get("/", response_model=List[FilialResponse])
async def get_filials_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):

    """
    Get a list of filials with the given details.
    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return await get_filials(db, skip, limit)


@router.get("/{filial_id}", response_model=FilialResponse)
async def get_filial_endpoint(filial_id: int, db: AsyncSession = Depends(get_db)):

    """
    Get a filial with the given ID.
    :param filial_id:
    :param db:
    :return:
    """
    return await get_filial(db, filial_id)


@router.get("/{filial_id}/{date}", response_model=[])
async def get_filial_employees_by_date_endpoint(filial_id: int, date: str, db: AsyncSession = Depends(get_db)):

    """
    Get a list of employees of a filial with the given ID by date.
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    return await get_filial_employees_by_date(db, filial_id, date)


@router.put("/{filial_id}", response_model=[])
async def update_filial_endpoint(filial_id: int, filial: FilialUpdate, db: AsyncSession = Depends(get_db)):

    """
    Update a filial with the given ID.
    :param filial_id:
    :param filial:
    :param db:
    """
    return await update_filial(db, filial_id, filial)


@router.delete("/{filial_id}")
async def delete_filial_endpoint(filial_id: int, db: AsyncSession = Depends(get_db)):

    """
    Delete a filial with the given ID.
    :param filial_id:
    :param db:
    """
    return await delete_filial(db, filial_id)