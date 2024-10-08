from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import current_user
from app.auth.db import User
from ..crud.attendance import create_attendance, get_attendances, get_commers_by_filial, get_commers_filials, \
    delete_attendance, get_commers_percentage, get_daily_attendance, get_attend_day
from ..database import get_db
from ..schemas import AttendanceDataResponse, AttendanceResponse

router = APIRouter()


@router.post("/", response_model=AttendanceResponse)
async def create_attendance_endpoint(
        person_id: int,
        camera_id: int,
        time: str,
        score: str,

        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)

):
    """
    Create a new attendance with the given details.
    :param user:
    :param score:
    :param time:
    :param person_id:
    :param camera_id:
    :param file:
    :param db:
    :return:
    """

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await create_attendance(db, file, person_id, camera_id, time, score)


@router.get("/", response_model=AttendanceDataResponse)
async def get_attendances_endpoint(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Get a list of attendances with the given details.
    :param user:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_attendances(db)


@router.get("/commers/{filial_id}/{date}", response_model=[])
async def get_commers_by_filial_endpoint(
        date: str, filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Get the commers for the given date.
    :param user:
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_commers_by_filial(db, date, filial_id)


@router.get("/commers/{date}", response_model=[])
async def get_commers_filials_endpoint(
        date: str,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
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


@router.get("/commers-percent/{date}", response_model=[])
async def get_commers_percentage_endpoint(
        date: str, filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Get the commers percentage for the given date.
    :param user:
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_commers_percentage(db, date, filial_id)


@router.get("/daily/{date}", response_model=[])
async def get_daily_attendance_endpoint(
        date: str, filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Get the daily attendance for the given date.
    :param user:
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_daily_attendance(db, date, filial_id)


@router.get("/attend-day/{date}", response_model=[])
async def get_attend_day_endpoint(
        date: str,
        filial_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Get the attendance for the given date.
    :param user:
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_attend_day(db, date, filial_id)


@router.delete("/delete/{attendance_id}", response_model=[])
async def delete_attendance_endpoint(
        attendance_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)):
    """
    Delete an attendance with the given ID.
    :param user:
    :param attendance_id:
    :param db:
    :return:
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await delete_attendance(db, attendance_id)



