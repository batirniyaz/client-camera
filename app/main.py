from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from .api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="A simple API to manage employees.",
    version="0.1"
)

app.include_router(router)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")
