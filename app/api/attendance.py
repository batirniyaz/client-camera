from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.attendance import create_attendance
from ..database import get_db
from ..schemas import AttendanceCreate, AttendanceResponse

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
