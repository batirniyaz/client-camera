from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth import auth_backend, current_user, fastapi_users
from app.auth.db import User
from app.database import engine, Base, SessionLocal, create_session
from app.api import router
from app.auth.schema import UserRead, UserCreate


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

main_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

main_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@main_app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

