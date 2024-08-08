from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate


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
    return result.scalars().all()


async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).filter_by(id=employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


async def update_employee(db: AsyncSession, employee_id: int, employee: EmployeeUpdate):
    db_employee = await get_employee(db, employee_id)
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
