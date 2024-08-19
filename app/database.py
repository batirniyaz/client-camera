import os

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not all([DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT]):
    raise ValueError("One or more environment variables are missing")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_URL = os.getenv("BASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=10, pool_timeout=30, pool_recycle=1800)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
Base: DeclarativeMeta = declarative_base()


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        print("Creating session")
        yield db
    finally:
        await db.close()
        print("Closing session")
