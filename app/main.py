from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from .api import router

app = FastAPI(
    title="Employee Management API",
    description="A simple API to manage employees.",
    version="0.1"
)

app.include_router(router)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()