from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.database import create_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async for db in create_session():
        yield db

main_app = FastAPI(
    title="Employee Management API",
    description="A simple API to manage employees.",
    version="0.1",
    lifespan=lifespan,
)

origins = ["*"]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(router)
main_app.mount("/storage", StaticFiles(directory="app/storage"), name="storage")


