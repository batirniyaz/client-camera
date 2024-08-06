from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres+asyncpg:happynation@localhost:5432/db_employee"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base: DeclarativeMeta = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
