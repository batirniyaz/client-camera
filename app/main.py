from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from .api import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
