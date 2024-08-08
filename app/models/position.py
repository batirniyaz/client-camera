import datetime

from sqlalchemy import text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING
from ..database import Base

if TYPE_CHECKING:
    from .employee import Employee


class Position(Base):
    __tablename__ = 'positions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)

    employees: Mapped[list["Employee"]] = relationship(back_populates="position", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=text("TIMEZONE('utc', now())"))
