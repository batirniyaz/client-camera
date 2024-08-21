from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
                "position_id": employee.position_id,
                "working_graphic_id": employee.working_graphic_id,
                "filial_id": employee.filial_id,
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
                "position_id": employee.position_id,
                "working_graphic_id": employee.working_graphic_id,
                "filial_id": employee.filial_id,
                "created_at": employee.created_at,
                "updated_at": employee.updated_at,
            } for employee in employees
        ],
        created_at=filial.created_at,
        updated_at=filial.updated_at,
    )

    return formatted_filial


async def get_filial_employees_by_date(db: AsyncSession, filial_id: int, date: str):
    result = await db.execute(select(Employee).filter_by(filial_id=filial_id))
    employees = result.scalars().all()
    if not employees:
        raise HTTPException(status_code=404, detail="Employees not found")

    formatted_filial_employees = []
    for filial_employee in employees:
        attendance_results = await db.execute(select(Attendance).filter_by(person_id=filial_employee.id))
        attendances = attendance_results.scalars().all()
        formatted_filial_employees.extend(attendances)

    formatted_date_employees = []
    for employee in formatted_filial_employees:
        employee_created_at = make_naive(employee.created_at)
        employee_date = datetime.fromisoformat(str(employee_created_at)).date().isoformat()
        if date.startswith(employee_date[:7]) if len(date) == 7 else date == employee_date:
            formatted_date_employees.append(employee)

    formatted_employees = {}
    for employee in formatted_date_employees:
        result = await db.execute(select(Employee).filter_by(id=employee.person_id))
        employee_data = result.scalar_one_or_none()
        if not employee_data:
            raise HTTPException(status_code=404, detail="Employee not found")
        formatted_employees[employee.person_id] = employee_data

    position_result = await db.execute(select(Position))
    positions = position_result.scalars().all()

    filial_result = await db.execute(select(Filial))
    filials = filial_result.scalars().all()

    response_model = [
        {
            "success": True,
            "total": len(formatted_date_employees),
            "data": [
                {
                    "id": attendance.id,
                    "employee": {"id": attendance.person_id, "name": formatted_employees[attendance.person_id].name},
                    "main_image": f"{BASE_URL}{formatted_employees[attendance.person_id].images[0].image_url}",
                    "position": {"id": formatted_employees[attendance.person_id].position_id, "name": positions[formatted_employees[attendance.person_id].position_id].name},
                    "filial": {"id": formatted_employees[attendance.person_id].filial_id, "name": filials[formatted_employees[attendance.person_id].filial_id].name},
                    "score": attendance.score,
                    "time": attendance.time,
                    "attendance_image": f"{BASE_URL}{attendance.file_path}",
                    "camera_id": attendance.camera_id,
                    "created_at": attendance.created_at,
                    "updated_at": attendance.updated_at,
                } for attendance in formatted_date_employees
            ]
        }
    ]
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
