from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.attendance import create_attendance, get_attendances, get_commers_by_filial, get_commers_filials, \
    delete_attendance, get_commers_percentage
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

):
    """
    Create a new attendance with the given details.
    :param score:
    :param time:
    :param person_id:
    :param camera_id:
    :param file:
    :param db:
    :return:
    """
    return await create_attendance(db, file, person_id, camera_id, time, score)


@router.get("/", response_model=AttendanceDataResponse)
async def get_attendances_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Get a list of attendances with the given details.
    :param db:
    :return:
    """
    return await get_attendances(db)


@router.get("/commers/{filial_id}/{date}", response_model=[])
async def get_commers_by_filial_endpoint(date: str, filial_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get the commers for the given date.
    :param filial_id:
    :param date:
    :param db:
    :return:
    """
    return await get_commers_by_filial(db, date, filial_id)


@router.get("/commers/{date}", response_model=[])
async def get_commers_filials_endpoint(date: str, db: AsyncSession = Depends(get_db)):
    """
    Get the commers for the given date.
    :param date:
    :param db:
    :return:
    """
    return await get_commers_filials(db, date)


@router.get("/commers-percent/{date}", response_model=[])
async def get_commers_percentage_endpoint(date: str, db: AsyncSession = Depends(get_db)):
    """
    Get the commers percentage for the given date.
    :param date:
    :param db:
    :return:
    """
    return await get_commers_percentage(db, date)


@router.delete("/delete/{attendance_id}", response_model=[])
async def delete_attendance_endpoint(attendance_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an attendance with the given ID.
    :param attendance_id:
    :param db:
    :return:
    """
    return await delete_attendance(db, attendance_id)



