import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeImage(Base):
    __tablename__ = 'employee_images'

    image_id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"))
    device_id = Column(Integer, default=0)
    employee = relationship("Employee", back_populates="images")

    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now(datetime.UTC))


