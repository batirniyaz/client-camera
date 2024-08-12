from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud import get_users, get_user, create_user, update_user, delete_user
from ..database import get_db
from ..schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user with the given details.
    :param user:
    :param db:
    :return:
    """
    return await create_user(db, user)


@router.get("/", response_model=list[UserResponse])
async def get_users_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Get a list of users with the given details.
    :param db:
    :return:
    """
    return await get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a user with the given details.
    :param user_id:
    :param db:
    :return:
    """
    return await get_user(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a user with the given details.
    :param user_id:
    :param user:
    :param db:
    :return:
    """
    return await update_user(db, user_id, user)


@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user with the given details.
    :param user_id:
    :param db:
    :return:
    """
    return await delete_user(db, user_id)
