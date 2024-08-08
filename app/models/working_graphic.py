import datetime

from sqlalchemy import text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING
from ..database import Base

if TYPE_CHECKING:
    from .employee import Employee


class WorkingGraphic(Base):
    __tablename__ = 'working_graphics'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    monday: Mapped[str] = mapped_column(default="9:00-19:00")
    tuesday: Mapped[str] = mapped_column(default="9:00-19:00")
    wednesday: Mapped[str] = mapped_column(default="9:00-19:00")
    thursday: Mapped[str] = mapped_column(default="9:00-19:00")
    friday: Mapped[str] = mapped_column(default="9:00-19:00")
    saturday: Mapped[str] = mapped_column(default="9:00-19:00")
    sunday: Mapped[str] = mapped_column(default="9:00-19:00")

    employees: Mapped[list["Employee"]] = relationship(back_populates="working_graphic", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=datetime.datetime.now(datetime.UTC))
