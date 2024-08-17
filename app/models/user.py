import datetime

# from fastapi_users import FastAPIUsers, models, schemas
# from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
# from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))


# class User(models.BaseUser, models.BaseOAuthAccountMixin):
#     name: str
#     email: str
#     phone_number: str
