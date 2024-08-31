
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, BASE_URL


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_URL = BASE_URL

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=10, pool_timeout=30,
                             pool_recycle=1800)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
Base: DeclarativeMeta = declarative_base()


async def create_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        print("Creating session")
        yield db
    finally:
        await db.close()
        print("Closing session")


async def get_db():
    async for db in create_session():
        yield db
