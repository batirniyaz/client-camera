import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional

from ..database import Base

if TYPE_CHECKING:
    from .employee_image import EmployeeImage
    from .position import Position
    from .working_graphic import WorkingGraphic
    from .filial import Filial


class Employee(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    phone_number: Mapped[str] = mapped_column(index=True)
    images: Mapped[list["EmployeeImage"]] = relationship(back_populates="employee", lazy="selectin")

    position_id: Mapped[int] = mapped_column(ForeignKey('positions.id'))
    position: Mapped[list["Position"]] = relationship(back_populates="employees", lazy="selectin")

    working_graphic_id: Mapped[Optional[int]] = mapped_column(ForeignKey('working_graphics.id'), nullable=True)
    working_graphic: Mapped[list["WorkingGraphic"]] = relationship(back_populates="employees",
                                                                   lazy="selectin")

    filial_id: Mapped[int] = mapped_column(ForeignKey('filials.id'), nullable=True)
    filial: Mapped[list["Filial"]] = relationship(back_populates="employees", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))
