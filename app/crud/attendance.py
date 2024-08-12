import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Attendance, Employee
from ..schemas.attendance import AttendanceDataResponse, AttendanceUpdate, AttendanceResponse, Image, AttendanceData
from ..utils.file_utils import save_upload_file


async def create_attendance(db: AsyncSession, file: UploadFile, person_id: int, camera_id: int, time: str, score: str):
    try:
        main_image_url = f"/storage/users/"
        dir_path = f"{main_image_url}{person_id}"

        if not os.path.exists(dir_path):
            os.makedirs(f"{dir_path}/images")

        file_path = save_upload_file(file, employee_id=person_id)
        image_url = f"{main_image_url}{person_id}/images/{file_path}"

        db_attendance = Attendance(
            person_id=person_id,
            camera_id=camera_id,
            time=time,
            score=score,
            file_path=image_url
        )
        db.add(db_attendance)
        await db.commit()
        await db.refresh(db_attendance)

        return AttendanceResponse.model_validate(db_attendance)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_attendances(db: AsyncSession):
    result = await db.execute(select(Employee).options(selectinload(Employee.images)))
    attendances = result.scalars().all()

    data = []
    for attendance in attendances:
        images = [Image(id=image.image_id, url=image.image_url) for image in attendance.images]
        data.append(AttendanceData(id=attendance.id, images=images))

    return AttendanceDataResponse(total=len(data), data=data)