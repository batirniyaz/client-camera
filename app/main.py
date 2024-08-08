from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from .database import engine, Base, SessionLocal
from .api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        print("Creating session")
        yield db
    finally:
        await db.close()
        print("Closing session")

main_app = FastAPI(
    title="Employee Management API",
    description="A simple API to manage employees.",
    version="0.1",
    lifespan=lifespan,
)

main_app.include_router(router)
main_app.mount("/storage", StaticFiles(directory="storage"), name="storage")

