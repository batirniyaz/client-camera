from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, index=True)
    timestamp = Column(String, index=True)

    image_url = relationship("EmployeeImage", back_populates="employee")
