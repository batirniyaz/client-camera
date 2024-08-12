import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class Attendance(Base):
    __tablename__ = 'attendances'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    file_path: Mapped[str] = mapped_column()
    camera_id: Mapped[int] = mapped_column()
    time: Mapped[str] = mapped_column()
    score: Mapped[str] = mapped_column()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))

