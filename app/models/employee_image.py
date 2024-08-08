import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING
from ..database import Base

if TYPE_CHECKING:
    from .employee import Employee

class EmployeeImage(Base):
    __tablename__ = 'employee_images'

    image_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_url: Mapped[str] = mapped_column(index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    device_id: Mapped[int] = mapped_column(default=0)
    employee: Mapped[list["Employee"]] = relationship(back_populates="images", lazy="selectin")

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=datetime.datetime.now(datetime.UTC))
