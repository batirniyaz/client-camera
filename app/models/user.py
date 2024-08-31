import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class User:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column()
    is_verified: Mapped[bool] = mapped_column()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))
