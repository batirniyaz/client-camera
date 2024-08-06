import datetime

from sqlalchemy import Column, Integer, String, text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class WorkingGraphic(Base):
    __tablename__ = 'working_graphics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    monday = Column(String, default="9:00-19:00")
    tuesday = Column(String, default="9:00-19:00")
    wednesday = Column(String, default="9:00-19:00")
    thursday = Column(String, default="9:00-19:00")
    friday = Column(String, default="9:00-19:00")
    saturday = Column(String, default="9:00-19:00")
    sunday = Column(String, default="9:00-19:00")

    employees = relationship("Employee", back_populates="working_graphic")

    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"),
                        onupdate=datetime.datetime.now(datetime.UTC))
