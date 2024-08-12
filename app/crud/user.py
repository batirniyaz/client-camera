from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import User
from ..schemas import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def login_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).filter_by(email=email, password=password))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    db_user = await get_user(db, user_id)
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return {"message": f"User {user_id} deleted"}
