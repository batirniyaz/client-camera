from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..crud.attendance import get_commers_by_filial
from ..database import BASE_URL
from ..models import Employee, Attendance, Position
from ..models.filial import Filial
from ..schemas.filial import FilialCreate, FilialUpdate, FilialResponse
from .client import make_naive


async def create_filial(db: AsyncSession, filial: FilialCreate):
    try:
        db_filial = Filial(**filial.model_dump())
        db.add(db_filial)
        await db.commit()
        await db.refresh(db_filial)

        return db_filial
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_filials(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Filial).offset(skip).limit(limit))
    filials = result.scalars().all()

    formatted_filials = []
    for filial in filials:
        employees_result = await db.execute(select(Employee).filter_by(filial_id=filial.id))
        employees = employees_result.scalars().all()

        formmated_employees = [
            {
                "id": employee.id,
                "name": employee.name,
                "phone_number": employee.phone_number,
                "position": employee.position.name,
                "working_graphic": {
                    "id": f"{employee.working_graphic_id}",
                    "name": f"{employee.working_graphic.name}",
                    "days": {
                        day.day: {
                            "id": day.id,
                            "day": day.day,
                            "time_in": day.time_in,
                            "time_out": day.time_out
                        } for day in employee.working_graphic.days
                    } if employee.working_graphic else None
                } if employee.working_graphic else None,
                "filial": employee.filial.name,
                "images": [
                    {
                        "id": image.image_id,
                        "url": f"{BASE_URL}{image.image_url}"
                    } for image in employee.images
                ],
                "created_at": employee.created_at,
                "updated_at": employee.updated_at,
            } for employee in employees
        ]

        formatted_filial = FilialResponse(
            id=filial.id,
            name=filial.name,
            address=filial.address,
            employees=formmated_employees,
            created_at=filial.created_at,
            updated_at=filial.updated_at,
        )
        formatted_filials.append(formatted_filial)

    return formatted_filials


async def get_filial(db: AsyncSession, filial_id: int):
    result = await db.execute(select(Filial).filter_by(id=filial_id))
    filial = result.scalar_one_or_none()
    if not filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    employees_result = await db.execute(select(Employee).filter_by(filial_id=filial.id))
    employees = employees_result.scalars().all()

    formatted_filial = FilialResponse(
        id=filial.id,
        name=filial.name,
        address=filial.address,
        employees=[
            {
                "id": employee.id,
                "name": employee.name,
                "phone_number": employee.phone_number,
                "position": {"id": employee.position_id, "name": f"{employee.position.name}"},
                "working_graphic": {
                    "id": f"{employee.working_graphic_id}",
                    "name": f"{employee.working_graphic.name}",
                    "days": {
                        day.day: {
                            "id": day.id,
                            "day": day.day,
                            "time_in": day.time_in,
                            "time_out": day.time_out
                        } for day in employee.working_graphic.days
                    } if employee.working_graphic else None
                } if employee.working_graphic else None,
                "filial": employee.filial.name,
                "images": [
                    {
                        "id": image.image_id,
                        "url": f"{BASE_URL}{image.image_url}"
                    } for image in employee.images
                ],
                "created_at": employee.created_at,
                "updated_at": employee.updated_at,
            } for employee in employees
        ],
        created_at=filial.created_at,
        updated_at=filial.updated_at,
    )

    return formatted_filial


async def get_filial_employees_by_date(db: AsyncSession, filial_id: int, date: str, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Employee).filter_by(filial_id=filial_id).offset(skip).limit(limit))
    employees = result.scalars().all()
    if not employees:
        raise HTTPException(status_code=404, detail="Employees not found")

    formatted_date_employees = []
    for employee in employees:
        attendance_results = await db.execute(select(Attendance).filter_by(person_id=employee.id))
        attendances = attendance_results.scalars().all()

        for attendance in attendances:
            attendance_date = make_naive(attendance.created_at).date().isoformat()
            if date.startswith(attendance_date[:7]) if len(date) == 7 else date == attendance_date:
                formatted_date_employees.append(attendance)

    if not formatted_date_employees:
        return ["Not found"]

    formatted_employees = {employee.id: employee for employee in employees}

    position_result = await db.execute(select(Position))
    positions = {position.id: position for position in position_result.scalars().all()}

    filial_result = await db.execute(select(Filial).filter_by(id=filial_id))
    filial = filial_result.scalar_one_or_none()
    if not filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    response_model = {
        "success": True,
        "total": len(formatted_date_employees),
        "data": [
            {
                "id": attendance.id,
                "employee": {"id": attendance.person_id, "name": formatted_employees[attendance.person_id].name},
                "main_image": f"{BASE_URL}{formatted_employees[attendance.person_id].images[0].image_url}"
                if formatted_employees[attendance.person_id].images else None,
                "position": {"id": formatted_employees[attendance.person_id].position_id,
                             "name": positions[formatted_employees[attendance.person_id].position_id].name},
                "filial": {"id": filial.id, "name": filial.name},
                "score": attendance.score,
                "time": attendance.time,
                "attendance_image": f"{BASE_URL}{attendance.file_path}",
                "camera_id": attendance.camera_id if attendance.camera_id else None,
                "created_at": attendance.created_at,
                "updated_at": attendance.updated_at,
            } for attendance in formatted_date_employees
        ]
    }
    return response_model


async def update_filial(db: AsyncSession, filial_id: int, filial: FilialUpdate):
    result = await db.execute(select(Filial).filter_by(id=filial_id))
    db_filial = result.scalar_one_or_none()

    if not db_filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    for key, value in filial.model_dump(exclude_unset=True).items():
        setattr(db_filial, key, value)

    await db.commit()
    await db.refresh(db_filial)
    return db_filial


async def delete_filial(db: AsyncSession, filial_id: int):
    result = await db.execute(select(Filial).filter_by(id=filial_id))
    db_filial = result.scalar_one_or_none()

    if not db_filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    await db.delete(db_filial)
    await db.commit()
    return {"message": f"Filial {filial_id} deleted"}


async def get_commers_filials(db: AsyncSession, date: str):
    result = await db.execute(select(Filial))
    filials = result.scalars().all()
    if not filials:
        raise HTTPException(status_code=404, detail="Filials not found")

    formatted_filials = []
    for filial in filials:
        filial_commers = await get_commers_by_filial(db, date, filial.id)
        formatted_filials.append({"filial_id": filial.id, "filial_name": filial.name, "filial_address": filial.address, "total_emp": len(filial.employees), "data": filial_commers})

    return formatted_filials
