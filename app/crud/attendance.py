import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Attendance
from ..schemas.attendance import AttendanceCreate, AttendanceUpdate
from ..utils.file_utils import save_upload_file


async def create_attendance(db: AsyncSession, attendance: AttendanceCreate, file: UploadFile):
    try:
        main_image_url = f"/storage/users/"
        if not os.path.exists(f"{main_image_url}{attendance.person_id}"):
            os.makedirs(f"{main_image_url}{attendance.person_id}")

        file_path = save_upload_file(file)
        image_url = f"{main_image_url}{attendance.person_id}/images/{file_path}"

        db_attendance = Attendance(
            person_id=attendance.person_id,
            camera_id=attendance.camera_id,
            time=attendance.time,
            score=attendance.score,
            file_path=image_url
        )
        db.add(db_attendance)
        await db.commit()
        await db.refresh(db_attendance)

        return db_attendance
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
