from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..models.employee_image import EmployeeImage
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
from ..schemas.employee_image import EmployeeImageResponse, EmployeeImageResponseModel


def create_employee(db: Session, employee: EmployeeCreate):
    try:
        db_employee = Employee(
            name=employee.name,
            phone_number=employee.phone_number,
            position_id=employee.position_id,
            filial_id=employee.filial_id,
            time_in=employee.time_in,
            time_out=employee.time_out
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        return db_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# def create_employee_image(db: Session, employee_image: EmployeeImageCreate):
#
#     try:
#         db_image = EmployeeImage(image_id=employee_image.employee_id, image_url=employee_image.image_url, employee_id=employee_image.employee_id)
#         db.add(db_image)
#         db.commit()
#         db.refresh(db_image)
#
#         response_data = EmployeeImageResponse(
#             employee_id=db_image.employee_id,
#             image_url=db_image.image_url
#         )
#
#         return EmployeeImageResponseModel(
#             status="success",
#             message="Image created successfully",
#             data=response_data
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Employee).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def store_employee_image(db: Session, employee_id: int, image_url: str):
    try:
        db_image = EmployeeImage(image_url=image_url, employee_id=employee_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        response_data = EmployeeImageResponse(
            employee_id=db_image.employee_id,
            image_id=db_image.image_id,
            image_url=db_image.image_url
        )

        return EmployeeImageResponseModel(
            status="success",
            message="Image stored successfully",
            data=response_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": f"Employee {employee} deleted"}


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db_employee.name = employee.name
    db_employee.phone_number = employee.phone_number
    db_employee.position_id = employee.position_id
    db_employee.filial_id = employee.filial_id
    db_employee.time_in = employee.time_in
    db_employee.time_out = employee.time_out
    db.commit()
    db.refresh(db_employee)
    return db_employee
