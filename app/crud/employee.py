from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..models.employee_image import EmployeeImage
from ..schemas.employee import EmployeeCreate


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name, phone_number=employee.phone_number)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    for image in employee.images:
        db_image = EmployeeImage(image_url=image.image_url, employee_id=db_employee.id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        db_employee.images.append(db_image)

    return db_employee


def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Employee).offset(skip).limit(limit).all()


def store_employee_image(db: Session, employee_id: int, image_url: str):
    db_image = EmployeeImage(image_url=image_url, employee_id=employee_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
