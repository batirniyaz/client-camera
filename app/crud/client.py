from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import Client
from ..schemas import ClientResponse, ClientCreate


async def create_client(db: AsyncSession, client: ClientCreate):

    result = await db.execute(select(Client).filter_by(id=client.id))
    from_db_client = result.scalar_one_or_none()

    if from_db_client is not None:
        from_db_client.client_status = "regular"
        from_db_client.age = int((from_db_client.age + client.age) / 2)
        from_db_client.time = client.time
        db_client = from_db_client
    else:
        db_client = Client(**client.model_dump())
        db_client.client_status = "new"

    try:
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error occurred") from e

    return ClientResponse.model_validate(db_client)
