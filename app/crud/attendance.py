import os
from datetime import datetime, timedelta

from fastapi import HTTPException, UploadFile
from sqlalchemy import func
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
        img_type = "attendances"

        if not os.path.exists(dir_path):
            os.makedirs(f"{dir_path}/{img_type}")

        file_path = save_upload_file(file, employee_id=person_id, img_type=img_type)
        image_url = f"{main_image_url}{person_id}/{img_type}/{file_path}"

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


async def get_commers_by_filial(db: AsyncSession, date: str, filial_id: int):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    result = await db.execute(select(Attendance))
    attendances = result.scalars().all()

    formatted_date_attendances = [
        attendance for attendance in attendances
        if (len(date) == 7 and date.startswith(parse_datetime(attendance.time).date().isoformat()[:7]))
           or (len(date) != 7 and date == parse_datetime(attendance.time).date().isoformat())
    ]

    first_attendances = {}
    for attendance in formatted_date_attendances:
        if attendance.person_id not in first_attendances:
            first_attendances[attendance.person_id] = attendance
        elif parse_datetime(first_attendances[attendance.person_id].time) > parse_datetime(attendance.time):
            first_attendances[attendance.person_id] = attendance

    on_time_commers = []
    late_commers = []
    did_not_come = []

    for person_id, attendance in first_attendances.items():
        result = await db.execute(select(Employee).filter_by(id=attendance.person_id))
        employee = result.scalar_one_or_none()
        if not employee or employee.filial_id != filial_id:
            continue

        attendance_datetime = parse_datetime(attendance.time)
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
            if isinstance(day.time_in, str):
                day.time_in = datetime.strptime(day.time_in, "%H:%M:%S").time()

            if attendance_time <= day.time_in.isoformat():
                early_come_to_n_minute = (datetime.combine(date_obj,
                                                           day.time_in) - attendance_datetime).total_seconds() // 60
                on_time_commers.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "employee_filial": employee.filial.name,
                        "employee_time_in": day.time_in,
                        "employee_time_out": day.time_out,
                        "early_come_to_n_minute": early_come_to_n_minute
                    }
                )
                day_found = True
                break
            elif attendance_time > day.time_in.isoformat():
                late_commers.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "attendance_time": attendance_time,
                        "late_to_n_minute": (attendance_datetime - datetime.combine(date_obj,
                                                                                    day.time_in)).total_seconds() // 60,
                        "employee_time_in": day.time_in,
                    }
                )

    unique_late_commers = {f"{commer['employee_id']}_{commer['attendance_time']}": commer for commer in late_commers}
    late_commers = list(unique_late_commers.values())

    all_employees = await db.execute(select(Employee).filter_by(filial_id=filial_id))
    all_employees = all_employees.scalars().all()

    attended_employees = {attendance.person_id for attendance in first_attendances.values()}
    for employee in all_employees:
        if employee.id not in attended_employees:
            if employee.working_graphic and employee.working_graphic.days:
                did_not_come.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "employee_filial": employee.filial.name,
                        "employee_time_in": employee.working_graphic.days[0].time_in,
                        "employee_time_out": employee.working_graphic.days[0].time_out,
                        "employee_phone_number": employee.phone_number
                    }
                )

    response_model = [
        {
            "success": True,
            "total": len(on_time_commers) + len(late_commers) + len(did_not_come),
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


async def get_commers_filials(db: AsyncSession, date: str):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    result = await db.execute(select(Attendance))
    attendances = result.scalars().all()

    formatted_date_attendances = [
        attendance for attendance in attendances
        if (len(date) == 7 and date.startswith(parse_datetime(attendance.time).date().isoformat()[:7]))
           or (len(date) != 7 and date == parse_datetime(attendance.time).date().isoformat())
    ]

    first_attendances = {}
    for attendance in formatted_date_attendances:
        if attendance.person_id not in first_attendances:
            first_attendances[attendance.person_id] = attendance
        elif parse_datetime(first_attendances[attendance.person_id].time) > parse_datetime(attendance.time):
            first_attendances[attendance.person_id] = attendance

    on_time_commers = []
    late_commers = []
    did_not_come = []

    all_employees = await db.execute(select(Employee))
    all_employees = all_employees.scalars().all()

    if not first_attendances:
        for employee in all_employees:
            if employee.working_graphic and employee.working_graphic.days:
                filial_employee_count = await db.execute(select(func.count(Employee.id)).filter_by(filial_id=employee.filial.id))
                filial_employee_count = filial_employee_count.scalar()
                did_not_come.append(
                    {
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "employee_position": employee.position.name,
                        "employee_time_in": employee.working_graphic.days[0].time_in,
                        "employee_time_out": employee.working_graphic.days[0].time_out,
                        "employee_phone_number": employee.phone_number,
                        "employee_filial": {
                            "id": employee.filial.id,
                            "name": employee.filial.name,
                            "address": employee.filial.address,
                            "filial_employees": filial_employee_count
                        },
                    }
                )
    else:
        for person_id, attendance in first_attendances.items():
            result = await db.execute(select(Employee).filter_by(id=attendance.person_id))
            employee = result.scalar_one_or_none()

            if not employee:
                continue

            attendance_datetime = parse_datetime(attendance.time)
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
                if isinstance(day.time_in, str):
                    day.time_in = datetime.strptime(day.time_in, "%H:%M:%S").time()

                if attendance_time <= day.time_in.isoformat():
                    early_come_to_n_minute = (datetime.combine(date_obj, day.time_in) - attendance_datetime).total_seconds() // 60
                    filial_employee_count = await db.execute(
                        select(func.count(Employee.id)).filter_by(filial_id=employee.filial.id))
                    filial_employee_count = filial_employee_count.scalar()
                    on_time_commers.append(
                        {
                            "employee_id": employee.id,
                            "employee_name": employee.name,
                            "employee_position": employee.position.name,
                            "employee_time_in": day.time_in,
                            "employee_time_out": day.time_out,
                            "early_come_to_n_minute": early_come_to_n_minute,
                            "employee_filial": {
                                "id": employee.filial.id,
                                "name": employee.filial.name,
                                "address": employee.filial.address,
                                "filial_employees": filial_employee_count
                            },
                        }
                    )
                    day_found = True
                    break
                elif attendance_time > day.time_in.isoformat():
                    late_to_n_minute = (attendance_datetime - datetime.combine(date_obj, day.time_in)).total_seconds() // 60
                    filial_employee_count = await db.execute(
                        select(func.count(Employee.id)).filter_by(filial_id=employee.filial.id))
                    filial_employee_count = filial_employee_count.scalar()
                    late_commers.append(
                        {
                            "employee_id": employee.id,
                            "employee_name": employee.name,
                            "employee_position": employee.position.name,
                            "attendance_time": attendance_time,
                            "late_to_n_minute": late_to_n_minute,
                            "employee_time_in": day.time_in,
                            "employee_filial": {
                                "id": employee.filial.id,
                                "name": employee.filial.name,
                                "address": employee.filial.address,
                                "filial_employees": filial_employee_count
                            },
                        }
                    )
                    day_found = True
                    break

        # attended_employees = {attendance.person_id for attendance in first_attendances.values()}
        # for employee in all_employees:
        #     if employee.id not in attended_employees:
        #         if employee.working_graphic and employee.working_graphic.days:
        #             did_not_come.append(
        #                 {
        #                     "employee_id": employee.id,
        #                     "employee_name": employee.name,
        #                     "employee_position": employee.position.name,
        #                     "employee_time_in": employee.working_graphic.days[0].time_in,
        #                     "employee_time_out": employee.working_graphic.days[0].time_out,
        #                     "employee_phone_number": employee.phone_number,
        #                     "employee_filial": {
        #                         "id": employee.filial.id,
        #                         "name": employee.filial.name,
        #                         "address": employee.filial.address,
        #                         "filial_employees": len(employee.filial.employees)
        #                     },
        #                 }
        #             )
    response_model = [
        {
            "success": True,
            "total": len(on_time_commers) + len(late_commers) + len(did_not_come),
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


async def get_commers_percentage(db: AsyncSession, date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m")
        year, month = date_obj.year, date_obj.month
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM")

    start_date = datetime(year, month, 1)
    end_date = start_date.replace(month=month % 12 + 1) if month != 12 else start_date.replace(year=year + 1, month=1)

    total_on_time = 0
    total_late = 0
    total_did_not_come = 0
    total_days = (end_date - start_date).days
    total_employees = 0

    current_date = start_date
    while current_date < end_date:
        daily_result = await get_commers_filials(db, current_date.strftime("%Y-%m-%d"))

        on_time_commers = daily_result[0]["on_time_commers"]["total"]
        late_commers = daily_result[0]["late_commers"]["total"]
        did_not_come = daily_result[0]["did_not_come"]["total"]

        total_on_time += on_time_commers
        total_late += late_commers
        total_did_not_come += did_not_come
        total_employees = max(total_employees, on_time_commers + late_commers + did_not_come)

        current_date += timedelta(days=1)

    if total_employees > 0:
        average_on_time_percentage = (total_on_time / (total_employees * total_days)) * 100
        average_late_percentage = (total_late / (total_employees * total_days)) * 100
        average_did_not_come_percentage = (total_did_not_come / (total_employees * total_days)) * 100
    else:
        average_on_time_percentage = average_late_percentage = average_did_not_come_percentage = 0

    response_model = {
        "success": True,
        "month": date_obj.strftime("%Y-%m"),
        "total_days": total_days,
        "average_on_time_percentage": average_on_time_percentage,
        "average_late_percentage": average_late_percentage,
        "average_did_not_come_percentage": average_did_not_come_percentage
    }

    return response_model


async def delete_attendance(db: AsyncSession, attendance_id: int):
    result = await db.execute(select(Attendance).filter_by(id=attendance_id))
    attendance = result.scalar_one_or_none()

    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")

    await db.delete(attendance)
    await db.commit()

    return {"success": True, "data": "Attendance deleted successfully"}


def parse_datetime(datetime_str):
    try:
        return datetime.fromisoformat(datetime_str)
    except ValueError:
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")