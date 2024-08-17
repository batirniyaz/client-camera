from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import Client
from ..schemas import ClientResponse, ClientCreate


async def create_client(db: AsyncSession, client: ClientCreate):

    result = await db.execute(select(Client).filter_by(id=client.id))
    from_db_client = result.scalar_one_or_none()

    db_client = Client(**client.model_dump())

    if from_db_client is not None:
        db_client.client_status = "regular"
        db_client.age = int((from_db_client.age + db_client.age) / 2)
        db_client.score = from_db_client.score
    else:
        db_client.client_status = "new"

    db.add(db_client)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

    await db.refresh(db_client)

    return ClientResponse.model_validate(db_client)
