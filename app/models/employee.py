import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True)
    time_in = Column(String)
    time_out = Column(String)
    images = relationship("EmployeeImage", back_populates="employee")

    position_id = Column(Integer, ForeignKey('positions.id'))
    position = relationship("Position", back_populates="employees")

    working_graphic_id = Column(Integer, ForeignKey('working_graphics.id'))
    working_graphic = relationship("WorkingGraphic", back_populates="employees")

    filial_id = Column(Integer, ForeignKey('filials.id'))
    filial = relationship("Filial", back_populates="employees")

    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now(datetime.UTC))