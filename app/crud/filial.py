from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.filial import Filial
from ..schemas.filial import FilialCreate, FilialUpdate


async def create_filial(db: AsyncSession, filial: FilialCreate):
    try:
        db_filial = Filial(**filial.model_dump())
        db.add(db_filial)
        await db.commit()
        await db.refresh(db_filial)

        return db_filial
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_filials(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Filial).offset(skip).limit(limit))
    return result.scalars().all()


async def get_filial(db: AsyncSession, filial_id: int):
    result = await db.execute(select(Filial).filter_by(id=filial_id))
    filial = result.scalar_one_or_none()
    if not filial:
        raise HTTPException(status_code=404, detail="Filial not found")
    return filial


async def update_filial(db: AsyncSession, filial_id: int, filial: FilialUpdate):
    db_filial = await get_filial(db, filial_id)
    for key, value in filial.model_dump(exclude_unset=True).items():
        setattr(db_filial, key, value)
    await db.commit()
    await db.refresh(db_filial)
    return db_filial


async def delete_filial(db: AsyncSession, filial_id: int):
    db_filial = await get_filial(db, filial_id)
    await db.delete(db_filial)
    await db.commit()
    return {"message": f"Filial {filial_id} deleted"}
