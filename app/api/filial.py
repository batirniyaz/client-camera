from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.auth.auth import current_user
from app.auth.db import User
from ..crud.filial import create_filial, get_filials, delete_filial, update_filial, get_filial, \
    get_filial_employees_by_date, get_commers_filials
from ..schemas.filial import FilialCreate, FilialResponse, FilialUpdate
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=FilialResponse)
async def create_filial_endpoint(
        filial: FilialCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):

    """
        Create a new filial with the given details.

        - **name**: The name of the filial
        - **address**: The address of the filial
        - **phone_number**: The phone number of the filial
        """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await create_filial(db, filial)


@router.get("/", response_model=List[FilialResponse])
async def get_filials_endpoint(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):

    """
    Get a list of filials with the given details.
    :param user:
    :param skip:
    :param limit:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return await get_filials(db, skip, limit)


@router.get("/{filial_id}", response_model=FilialResponse)
async def get_filial_endpoint(
        filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):

    """
    Get a filial with the given ID.
    :param user:
    :param filial_id:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_filial(db, filial_id)


@router.get("/{filial_id}/{date}", response_model=[])
async def get_filial_employees_by_date_endpoint(
        filial_id: int,
        date: str,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user),
        skip: int = 0,
        limit: int = 10,
):

    """
    Get a list of employees of a filial with the given ID by date.
    :param limit:
    :param skip:
    :param user:
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_filial_employees_by_date(db, filial_id, date, skip, limit)


@router.get("/commers/", response_model=[])
async def get_commers_filials_endpoint(
        db: AsyncSession = Depends(get_db),
        date: str = Query(...),
        user: User = Depends(current_user)
):

    """
    Get the commers for the given date.
    :param user:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_commers_filials(db, date)


@router.put("/{filial_id}", response_model=[])
async def update_filial_endpoint(
        filial_id: int,
        filial: FilialUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):

    """
    Update a filial with the given ID.
    :param user:
    :param filial_id:
    :param filial:
    :param db:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await update_filial(db, filial_id, filial)


@router.delete("/{filial_id}")
async def delete_filial_endpoint(
        filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):

    """
    Delete a filial with the given ID.
    :param user:
    :param filial_id:
    :param db:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await delete_filial(db, filial_id)
