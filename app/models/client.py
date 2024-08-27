
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, JSON
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


class DailyReport(Base):
    __tablename__ = 'daily_reports'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[str] = mapped_column()
    clients: Mapped[list[int]] = mapped_column(JSON, default=[])
    gender: Mapped[dict[str, int]] = mapped_column(JSON, default={"male": 0, "female": 0})
    age: Mapped[dict[str, int]] = mapped_column(JSON, default={})
    time_slots: Mapped[dict[str, int]] = mapped_column(JSON, default={})
    total_new_clients: Mapped[int] = mapped_column(default=0)
    total_regular_clients: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))