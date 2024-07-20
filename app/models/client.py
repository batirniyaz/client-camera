from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, index=True)
    timestamp = Column(String, index=True)
    is_regular = Column(Integer, index=True)

    image_url = relationship("EmployeeImage", back_populates="employee")


