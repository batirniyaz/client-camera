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

                working_graphic = WorkingGraphicResponse(
                    id=working_graphic.id,
                    name=working_graphic.name,
                    days=[
                        DayResponse(
                            id=day.id,
                            day=day.day,
                            time_in=day.time_in,
                            time_out=day.time_out,
                            is_work_day=day.is_work_day,
                            created_at=day.created_at,
                            updated_at=day.updated_at,
                        ) for day in days
                    ],
                    created_at=working_graphic.created_at,
                    updated_at=working_graphic.updated_at,
                )

        filial = await db.execute(select(Filial).filter_by(id=employee.filial_id))
        filial = filial.scalar_one_or_none()

        images = await db.execute(select(EmployeeImage).filter_by(employee_id=employee.id))
        images = images.scalars().all()

        formatted_employee = EmployeeResponse(
            id=employee.id,
            name=employee.name,
            phone_number=employee.phone_number,
            position_id=PositionResponse(
                id=position.id,
                name=position.name,
                created_at=position.created_at,
                updated_at=position.updated_at
            ),
            working_graphic=working_graphic,
            filial_id=FilialResponse(
                id=filial.id,
                name=filial.name,
                address=filial.address,
                created_at=filial.created_at,
                updated_at=filial.updated_at
            ),
            images=[
                EmployeeImageResponse(
                    image_id=image.image_id,
                    employee_id=image.employee_id,
                    image_url=f"{BASE_URL}{image.image_url}",
                    created_at=image.created_at,
                    updated_at=image.updated_at,
                ) for image in images
            ],
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
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

            working_graphic = WorkingGraphicResponse(
                id=working_graphic.id,
                name=working_graphic.name,
                days=[
                    DayResponse(
                        id=day.id,
                        day=day.day,
                        time_in=day.time_in,
                        time_out=day.time_out,
                        is_work_day=day.is_work_day,
                        created_at=day.created_at,
                        updated_at=day.updated_at,
                    ) for day in days
                ],
                created_at=working_graphic.created_at,
                updated_at=working_graphic.updated_at,
            )

    filial = await db.execute(select(Filial).filter_by(id=employee.filial_id))
    filial = filial.scalar_one_or_none()

    images = await db.execute(select(EmployeeImage).filter_by(employee_id=employee.id))
    images = images.scalars().all()

    formatted_employee = EmployeeResponse(
        id=employee.id,
        name=employee.name,
        phone_number=employee.phone_number,
        position_id=PositionResponse(
            id=position.id,
            name=position.name,
            created_at=position.created_at,
            updated_at=position.updated_at
        ),
        working_graphic=working_graphic,
        filial_id=FilialResponse(
            id=filial.id,
            name=filial.name,
            address=filial.address,
            created_at=filial.created_at,
            updated_at=filial.updated_at
        ),
        images=[
            EmployeeImageResponse(
                image_id=image.image_id,
                employee_id=image.employee_id,
                image_url=f"{BASE_URL}{image.image_url}",
                created_at=image.created_at,
                updated_at=image.updated_at,
            ) for image in images
        ],
        created_at=employee.created_at,
        updated_at=employee.updated_at
    )

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

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        await db.execute(delete(EmployeeImage).where(EmployeeImage.employee_id==employee_id))

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
        attendance_datetime = datetime.fromisoformat(db_attendance.time)
        attendance_date = attendance_datetime.strftime("%Y-%m")
        if attendance_date == date:
            formatted_date_attendances.append(db_attendance)

    # for formatted_date_attendance in formatted_date_attendances:
    #     attendance_response = [
    #         {
    #             "id": attendance.id,
    #             "time": attendance.time,
    #             "is_late": attendance.is_late,
    #             "created_at": attendance.created_at,
    #             "updated_at": attendance.updated_at
    #         } for attendance in formatted_date_attendances
    #     ]

    attendance_response = [

    ]

    response_model = [
        {
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
    ]

    return response_model
