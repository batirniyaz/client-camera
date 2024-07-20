from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..models.employee_image import EmployeeImage
from ..schemas.employee import EmployeeCreate


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(person_id=employee.person_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    for image in employee.image_url:
        db_image = EmployeeImage(**image.dict(), employee_id=db_employee.id)
        db.add(db_image)
    return db_employee