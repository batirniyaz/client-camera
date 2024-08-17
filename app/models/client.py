
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
import datetime

from ..database import Base


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gender: Mapped[str] = mapped_column()
    score: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    client_status: Mapped[str] = mapped_column()
    camera_id: Mapped[int] = mapped_column()
    time: Mapped[str] = mapped_column()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))