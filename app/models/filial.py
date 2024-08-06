import datetime
from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from ..database import Base


class Filial(Base):
    __tablename__ = 'filials'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    employees = relationship("Employee", back_populates="filial")

    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"),
                        onupdate=datetime.datetime.now(datetime.UTC))
