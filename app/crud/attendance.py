import os
from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Attendance, Employee, WorkingGraphic, Day
from ..schemas.attendance import AttendanceDataResponse, AttendanceResponse, Image, AttendanceData
from ..utils.file_utils import save_upload_file
from ..database import BASE_URL


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

        response = AttendanceResponse.model_validate(db_attendance)
        response.file_path = f"{BASE_URL}{image_url}"

        return response
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_attendances(db: AsyncSession):
    result = await db.execute(select(Employee).options(selectinload(Employee.images)))
    attendances = result.scalars().all()

    data = []
    for attendance in attendances:
        images = [Image(id=image.image_id, url=f"{BASE_URL}{image.image_url}") for image in attendance.images]
        data.append(AttendanceData(id=attendance.id, images=images))

    return AttendanceDataResponse(total=len(data), data=data)


async def get_commers(db: AsyncSession, date: str, filial_id: int):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    result = await db.execute(select(Attendance))
    attendances = result.scalars().all()

    formatted_date_attendances = [
        attendance for attendance in attendances
        if (len(date) == 7 and date.startswith(datetime.fromisoformat(attendance.time).date().isoformat()[:7]))
           or (len(date) != 7 and date == datetime.fromisoformat(attendance.time).date().isoformat())
    ]

    on_time_commers = []
    late_commers = []
    did_not_come = []

    formatted_filial_dates = []
    for attendance in formatted_date_attendances:
        result = await db.execute(select(Employee).filter_by(id=attendance.person_id))
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        if employee.filial_id == filial_id:
            formatted_filial_dates.append(attendance)

    for attendance in formatted_filial_dates:
        employee = await db.execute(select(Employee).filter_by(id=attendance.person_id))
        employee = employee.scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        attendance_datetime = datetime.fromisoformat(attendance.time)
        time = attendance_datetime.time()

        working_graphic = await db.execute(select(WorkingGraphic).filter_by(id=employee.working_graphic_id))
        working_graphic = working_graphic.scalar_one_or_none()
        if not working_graphic:
            raise HTTPException(status_code=404, detail="Working graphic not found")

        day_result = await db.execute(select(Day).filter_by(working_graphic_id=working_graphic.id))
        day = day_result.scalars().all()

        if not day:
            raise HTTPException(status_code=404, detail="Day not found")

        attendance_time = time.isoformat()
        day_found = False

        for day in day:
            if day.time_in <= attendance_time <= day.time_out:
                on_time_commers.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "employee_filial": employee.filial.name,
                        "employee_time_in": day.time_in,
                        "employee_time_out": day.time_out,
                        "early_come_to_n_minute": (datetime.strptime(day.time_in, "%H:%M:%S") - datetime.strptime(attendance_time, "%H:%M:%S")).seconds // 60
                    }
                )
                day_found = True
                break
            elif attendance_time > day.time_out:
                late_commers.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "attendance_time": attendance_time,
                        "late_to_n_minute": (datetime.strptime(attendance_time, "%H:%M:%S") - datetime.strptime(day.time_in, "%H:%M:%S")).seconds // 60,
                        "employee_time_in": day.time_in,
                    }
                )
                day_found = True
                break

        if not day_found:
            did_not_come.append(
                {
                    "employee_id": employee.id,
                    "employee_name": employee.name,
                    "employee_position": employee.position.name,
                    "employee_filial": employee.filial.name,
                    "employee_time_in": day.time_in,
                    "employee_time_out": day.time_out,
                    "employee_phone_number": employee.phone_number
                }
            )

    response_model = [
        {
            "success": True,
            "total": len(formatted_filial_dates),
            "on_time_commers": {
                "total": len(on_time_commers),
                "data": on_time_commers
            },
            "late_commers": {
                "total": len(late_commers),
                "data": late_commers
            },
            "did_not_come": {
                "total": len(did_not_come),
                "data": did_not_come
            }
        }
    ]

    return response_model


async def delete_attendance(db: AsyncSession, attendance_id: int):
    result = await db.execute(select(Attendance).filter_by(id=attendance_id))
    attendance = result.scalar_one_or_none()

    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")

    await db.delete(attendance)
    await db.commit()

    return {"success": True, "data": "Attendance deleted successfully"}
