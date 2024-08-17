import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING
from ..database import Base

if TYPE_CHECKING:
    from .employee import Employee

class Day(Base):
    __tablename__ = 'days'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day: Mapped[str] = mapped_column()
    time_in: Mapped[datetime.time] = mapped_column()
    time_out: Mapped[datetime.time] = mapped_column()
    is_work_day: Mapped[bool] = mapped_column()

    working_graphic_id: Mapped[int] = ForeignKey("working_graphics.id")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))


class WorkingGraphic(Base):
    __tablename__ = 'working_graphics'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()

    days: Mapped[list[Day]] = relationship(back_populates="working_graphic", lazy="selectin")
    employees: Mapped[list["Employee"]] = relationship(back_populates="working_graphic", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))
