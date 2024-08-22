from datetime import datetime

from fastapi import HTTPException
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
    db_employee = await get_employee(db, employee_id)

    if employee.position_id is not None:
        db_employee.position_id = employee.position_id.id

    if employee.working_graphic_id is not None:
        db_employee.working_graphic_id = employee.working_graphic_id.id

    if employee.filial_id is not None:
        db_employee.filial_id = employee.filial_id.id

    for key, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, key, value)

    await db.commit()
    await db.refresh(db_employee)

    position = employee.position_id
    working_graphic = employee.working_graphic_id
    filial = employee.filial_id

    images = await db.execute(select(EmployeeImage).filter_by(employee_id=db_employee.id))
    images = images.scalars().all()

    formatted_employee = EmployeeResponse(
        id=db_employee.id,
        name=db_employee.name,
        phone_number=db_employee.phone_number,
        position_id=position,
        filial_id=filial,
        working_graphic=working_graphic,
        images=[
            EmployeeImageResponse(
                image_id=image.image_id,
                employee_id=image.employee_id,
                image_url=f"{BASE_URL}{image.image_url}",
                created_at=image.created_at,
                updated_at=image.updated_at,
            ) for image in images
        ],
        created_at=db_employee.created_at,
        updated_at=db_employee.updated_at
    )

    return formatted_employee


async def delete_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    db_employee = result.scalar_one_or_none()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    await db.delete(db_employee)
    await db.commit()
    return {"message": f"Employee {employee_id} deleted"}


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
