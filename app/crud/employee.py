from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..models.employee_image import EmployeeImage
from ..schemas.employee import EmployeeCreate


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name, phone_number=employee.phone_number, position=employee.position)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Employee).offset(skip).limit(limit).all()


def store_employee_image(db: Session, employee_id: int, image_url: str):
    db_image = EmployeeImage(image_url=image_url, employee_id=employee_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def del_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": f"Employee {employee} deleted"}
