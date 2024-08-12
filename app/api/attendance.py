from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.attendance import create_attendance, get_attendances
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