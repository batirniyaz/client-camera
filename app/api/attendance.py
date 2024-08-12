from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.attendance import create_attendance
from ..database import get_db
from ..schemas import AttendanceCreate

router = APIRouter()


@router.post("/")
async def create_attendance_endpoint(attendance: AttendanceCreate, file: UploadFile, db: AsyncSession = Depends(get_db)):
    """
    Create a new attendance with the given details.
    :param attendance:
    :param file:
    :param db:
    :return:
    """
    return await create_attendance(db, attendance, file)
