from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    employees = relationship("Employee", back_populates="position")

    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))