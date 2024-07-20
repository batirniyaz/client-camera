from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True)
    position = Column(String, index=True)
    images = relationship("EmployeeImage", back_populates="employee")
