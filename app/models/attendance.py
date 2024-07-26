from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    score = Column(Integer)
    datetime = Column(String)
    created_at = Column(String)
    updated_at = Column(String)