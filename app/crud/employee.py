from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import DayResponse
from ..schemas import WorkingGraphicResponse, EmployeeImageResponse
from ..schemas.position import PositionResponse
from ..schemas.filial import FilialResponse
from ..models import Position, WorkingGraphic, Filial, Day, EmployeeImage, Attendance
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

from app.database import BASE_URL

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_employee(db: AsyncSession, employee: EmployeeCreate):
    try:
        db_employee = Employee(**employee.model_dump())
        db.add(db_employee)
        await db.commit()
        await db.refresh(db_employee)

        return db_employee
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Employee).offset(skip).limit(limit))
    employees = result.scalars().all()

    formatted_employees = []
    for employee in employees:
        position = await db.execute(select(Position).filter_by(id=employee.position_id))
        position = position.scalar_one_or_none()

        working_graphic = None
        if employee.working_graphic_id:
            working_graphic = await db.execute(select(WorkingGraphic).filter_by(id=employee.working_graphic_id))
            working_graphic = working_graphic.scalar_one_or_none()

            if working_graphic:
                days_result = await db.execute(select(Day).filter_by(working_graphic_id=working_graphic.id))
                days = days_result.scalars().all()

                working_graphic = {
                    "id": working_graphic.id,
                    "name": working_graphic.name,
                    "days": [
                        {
                            "id": day.id,
                            "day": day.day,
                            "time_in": day.time_in,
                            "time_out": day.time_out,
                            "is_work_day": day.is_work_day,
                        } for day in days
                    ],
                }

        filial = await db.execute(select(Filial).filter_by(id=employee.filial_id))
        filial = filial.scalar_one_or_none()

        images = await db.execute(select(EmployeeImage).filter_by(employee_id=employee.id))
        images = images.scalars().all()

        formatted_employee = {
            "id": employee.id,
            "name": employee.name,
            "phone_number": employee.phone_number,
            "position": {
                "id": position.id,
                "name": position.name,
            },
            "working_graphic": working_graphic,
            "filial": {
                "id": filial.id,
                "name": filial.name,
                "address": filial.address,
            },
            "images": [
                {
                    "image_id": image.image_id,
                    "employee_id": image.employee_id,
                    "image_url": f"{BASE_URL}{image.image_url}",
                } for image in images
            ],
        }
        formatted_employees.append(formatted_employee)

    return formatted_employees


async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    position = await db.execute(select(Position).filter_by(id=employee.position_id))
    position = position.scalar_one_or_none()

    working_graphic = None
    if employee.working_graphic_id:
        working_graphic = await db.execute(select(WorkingGraphic).filter_by(id=employee.working_graphic_id))
        working_graphic = working_graphic.scalar_one_or_none()

        if working_graphic:
            days_result = await db.execute(select(Day).filter_by(working_graphic_id=employee.working_graphic_id))
            days = days_result.scalars().all()

            working_graphic = {
                "id": working_graphic.id,
                "name": working_graphic.name,
                "days": [
                    {
                        "id": day.id,
                        "day": day.day,
                        "time_in": day.time_in,
                        "time_out": day.time_out,
                        "is_work_day": day.is_work_day,
                    } for day in days
                ],
            }

    filial = await db.execute(select(Filial).filter_by(id=employee.filial_id))
    filial = filial.scalar_one_or_none()

    images = await db.execute(select(EmployeeImage).filter_by(employee_id=employee.id))
    images = images.scalars().all()

    formatted_employee = {
        "id": employee.id,
        "name": employee.name,
        "phone_number": employee.phone_number,
        "position": {
            "id": position.id,
            "name": position.name,
        },
        "working_graphic": working_graphic,
        "filial": {
            "id": filial.id,
            "name": filial.name,
            "address": filial.address,
        },
        "images": [
            {
                "image_id": image.image_id,
                "employee_id": image.employee_id,
                "image_url": f"{BASE_URL}{image.image_url}",
            } for image in images
        ],
    }

    return formatted_employee


async def update_employee(db: AsyncSession, employee_id: int, employee: EmployeeUpdate):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    db_employee = result.scalar_one_or_none()

    if employee.position_id is not None:
        db_employee.position_id = employee.position_id

    if employee.working_graphic_id is not None:
        db_employee.working_graphic_id = employee.working_graphic_id

    if employee.filial_id is not None:
        db_employee.filial_id = employee.filial_id

    for key, value in employee.model_dump(exclude_unset=True).items():
        if key == "position_id":
            position = await db.execute(select(Position).filter_by(id=value))
            position = position.scalar_one_or_none()
            if not position:
                raise HTTPException(status_code=404, detail="Position not found")
            db_employee.position_id = position.id
        elif key == "filial_id":
            filial = await db.execute(select(Filial).filter_by(id=value))
            filial = filial.scalar_one_or_none()
            if not filial:
                raise HTTPException(status_code=404, detail="Filial not found")
            db_employee.filial_id = filial.id
        else:
            setattr(db_employee, key, value)

    await db.commit()
    await db.refresh(db_employee)

    formatted_employee = [
        {
            "id": db_employee.id,
            "name": db_employee.name,
            "phone_number": db_employee.phone_number,
            "position_id": db_employee.position_id,
            "working_graphic_id": db_employee.working_graphic_id,
            "filial_id": db_employee.filial_id,
        }
    ]

    return formatted_employee


def make_naive(dt):
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


async def delete_employee(db: AsyncSession, employee_id: int):
    try:
        result = await db.execute(select(Employee).filter_by(id=employee_id))
        db_employee = result.scalar_one_or_none()

        if not db_employee:
            logger.error(f"Employee {employee_id} not found")
            raise HTTPException(status_code=404, detail="Employee not found")

        await db.execute(delete(EmployeeImage).where(EmployeeImage.employee_id == employee_id))

        db_employee.updated_at = make_naive(datetime.now(timezone.utc))

        await db.delete(db_employee)
        await db.commit()
        logger.info(f"Employee {employee_id} deleted")
        return {"message": f"Employee {employee_id} deleted"}
    except Exception as e:
        logger.error(f"Error occurred while deleting employee: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_employee_deep(db: AsyncSession, employee_id: int, date: str):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    db_employee = result.scalar_one_or_none()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance_result = await db.execute(select(Attendance).filter_by(person_id=employee_id))
    db_attendances = attendance_result.scalars().all()
    if not db_attendances:
        raise HTTPException(status_code=404, detail="Attendances not found")

    formatted_date_attendances = []
    for db_attendance in db_attendances:
        try:
            attendance_datetime = datetime.strptime(db_attendance.time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Time data {db_attendance.time} does not match format %Y-%m-%d %H:%M:%S")

        attendance_date = attendance_datetime.strftime("%Y-%m")
        if attendance_date == date:
            formatted_date_attendances.append(db_attendance)

    if not formatted_date_attendances:
        raise HTTPException(status_code=404, detail="No attendances found for the specified date")

    daily_attendances = {}
    for attendance in formatted_date_attendances:
        attendance_date_str = datetime.strptime(attendance.time, "%Y-%m-%d %H:%M:%S").date().isoformat()
        if attendance_date_str not in daily_attendances:
            daily_attendances[attendance_date_str] = {
                'first': attendance,
                'last': attendance
            }
        else:
            if datetime.strptime(attendance.time, "%Y-%m-%d %H:%M:%S") < datetime.strptime(daily_attendances[attendance_date_str]['first'].time, "%Y-%m-%d %H:%M:%S"):
                daily_attendances[attendance_date_str]['first'] = attendance
            elif datetime.strptime(attendance.time, "%Y-%m-%d %H:%M:%S") > datetime.strptime(daily_attendances[attendance_date_str]['last'].time, "%Y-%m-%d %H:%M:%S"):
                daily_attendances[attendance_date_str]['last'] = attendance

    attendance_response = []
    for attendance_date_str, att in daily_attendances.items():
        date_obj = datetime.strptime(attendance_date_str, "%Y-%m-%d").date()

        weekday = date_obj.strftime("%A").lower()
        workday = next((day for day in db_employee.working_graphic.days if day.day == weekday), None)

        if workday:
            try:
                time_in = datetime.combine(date_obj, datetime.strptime(workday.time_in, "%H:%M:%S").time())
            except ValueError:
                time_in = datetime.combine(date_obj, datetime.strptime(workday.time_in, "%H:%M").time())
            try:
                time_out = datetime.combine(date_obj, datetime.strptime(workday.time_out, "%H:%M:%S").time())
            except ValueError:
                time_out = datetime.combine(date_obj, datetime.strptime(workday.time_out, "%H:%M").time())

            first_att = att['first']
            last_att = att['last']

            late_n_minute = int(
                (datetime.strptime(first_att.time, "%Y-%m-%d %H:%M:%S") - time_in).total_seconds() // 60)
            if late_n_minute < 0:
                late_n_minute = 0

            early_leave_n_minute = int(
                (time_out - datetime.strptime(last_att.time, "%Y-%m-%d %H:%M:%S")).total_seconds() // 60)
            if early_leave_n_minute < 0:
                early_leave_n_minute = 0

            attendance_response.append({
                "date": date_obj.isoformat(),
                "attend_time": datetime.strptime(first_att.time, "%Y-%m-%d %H:%M:%S").time().isoformat(),
                "attend_image": f"{BASE_URL}{first_att.file_path}",
                "late_n_minute": late_n_minute if late_n_minute > 0 else None,
                "early_leave_n_minute": early_leave_n_minute if early_leave_n_minute > 0 else None,
                "leave_time": datetime.strptime(last_att.time, "%Y-%m-%d %H:%M:%S").time().isoformat(),
                "leave_image": f"{BASE_URL}{first_att.file_path}",
            })

    response_model = {
        "id": employee_id,
        "name": db_employee.name,
        "phone_number": db_employee.phone_number,
        "position": db_employee.position.name,
        "working_graphic": {
            "id": f"{db_employee.working_graphic_id}",
            "name": f"{db_employee.working_graphic.name}",
            "days": {
                day.day: {
                    "id": day.id,
                    "day": day.day,
                    "time_in": day.time_in,
                    "time_out": day.time_out
                } for day in db_employee.working_graphic.days
            } if db_employee.working_graphic else None
        } if db_employee.working_graphic else None,
        "filial": db_employee.filial.name,
        "images": [
            {
                "id": image.image_id,
                "url": f"{BASE_URL}{image.image_url}"
            } for image in db_employee.images
        ],
        "attendances": attendance_response,
    }

    return response_model
