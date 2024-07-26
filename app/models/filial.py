from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base


class Filial(Base):
    __tablename__ = 'filials'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    employees = Column(Integer)
    device_id = Column(Integer)
    created_at = Column(String)