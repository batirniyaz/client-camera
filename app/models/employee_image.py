from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeImage(Base):
    __tablename__ = 'employee_images'

    image_id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    device_id = Column(Integer, default=0)
    employee = relationship("Employee", back_populates="images")

