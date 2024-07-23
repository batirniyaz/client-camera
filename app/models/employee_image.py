from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeImage(Base):
    __tablename__ = 'employee_images'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, nullable=False, default=0)
    image_url = Column(String, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    device_id = Column(Integer, nullable=False, default=0)
    employee = relationship("Employee", back_populates="images")

    __table_args__ = (UniqueConstraint('employee_id', 'image_id', name='unique_image_employee'),)
