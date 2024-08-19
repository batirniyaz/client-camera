from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Position, WorkingGraphic, Filial
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from ..schemas.position import PositionResponse
from ..schemas.working_graphic import WorkingGraphicResponse, DayResponse
from ..schemas.filial import FilialResponse
from ..schemas.employee_image import EmployeeImageResponse

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
        formatted_employee = EmployeeResponse(
            id=employee.id,
            name=employee.name,
            position=PositionResponse(
                id=employee.position.id,
                name=employee.position.name
            ),
            filial=FilialResponse(
                id=employee.filial.id,
                name=employee.filial.name
            ),
            phone_number=employee.phone_number,
            working_graphic=WorkingGraphicResponse(
                id=employee.working_graphic.id,
                name=employee.working_graphic.name,
                days=[
                    DayResponse(
                        id=day.id,
                        day=day.day,
                        time_in=day.time_in,
                        time_out=day.time_out,
                        is_working=day.is_work_day
                    ) for day in employee.working_graphic.days
                ]
            ) if employee.working_graphic else None,
            images=[
                EmployeeImageResponse(
                    id=image.image_id,
                    url=f"{BASE_URL}{image.image_url}"
                ) for image in employee.images
            ],
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
        formatted_employees.append(formatted_employee)

    return employees


async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for image in employee.images:
        image.image_url = f"{BASE_URL}{image.image_url}"

    return employee


async def update_employee(db: AsyncSession, employee_id: int, employee: EmployeeUpdate):
    db_employee = await get_employee(db, employee_id)

    if employee.position_id is not None:
        result = await db.execute(select(Position).filter_by(id=employee.position_id))
        position = result.scalar_one_or_none()
        if not position:
            raise HTTPException(status_code=400, detail=f"Position with ID {employee.position_id} not found")

    if employee.working_graphic_id is not None:
        result = await db.execute(select(WorkingGraphic).filter_by(id=employee.working_graphic_id))
        working_graphic = result.scalar_one_or_none()
        if not working_graphic:
            raise HTTPException(status_code=400,
                                detail=f"Working graphic with ID {employee.working_graphic_id} not found")

    if employee.filial_id is not None:
        result = await db.execute(select(Filial).filter_by(id=employee.filial_id))
        filial = result.scalar_one_or_none()
        if not filial:
            raise HTTPException(status_code=400, detail=f"Filial with ID {employee.filial_id} not found")

    for key, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, key, value)

    await db.commit()
    await db.refresh(db_employee)
    return db_employee


async def delete_employee(db: AsyncSession, employee_id: int):
    db_employee = await get_employee(db, employee_id)
    await db.delete(db_employee)
    await db.commit()
    return {"message": f"Employee {employee_id} deleted"}
