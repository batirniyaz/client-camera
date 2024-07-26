from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True)
    position_id = Column(Integer, index=True)
    filial_id = Column(Integer, ForeignKey("filials.id"))
    time_in = Column(String)
    time_out = Column(String)
    images = relationship("EmployeeImage", back_populates="employee")

