import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models import Employee


class Day(Base):
    __tablename__ = "days"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day: Mapped[str] = mapped_column()
    time_in: Mapped[str] = mapped_column()
    time_out: Mapped[str] = mapped_column()
    is_work_day: Mapped[bool] = mapped_column()

    working_graphic_id: Mapped[int] = mapped_column(ForeignKey("working_graphics.id"))
    working_graphic: Mapped["WorkingGraphic"] = relationship(back_populates="days", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))


class WorkingGraphic(Base):
    __tablename__ = "working_graphics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    days: Mapped[list["Day"]] = relationship( back_populates="working_graphic", lazy="selectin")
    employees: Mapped[list["Employee"]] = relationship(back_populates="working_graphic", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))
