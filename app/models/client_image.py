from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class ClientImage(Base):
    __tablename__ = "client_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="image_url")