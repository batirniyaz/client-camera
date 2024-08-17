from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Client, DailyReport
from ..schemas import ClientResponse, ClientCreate, DailyReportResponse, DailyReportCreate
import logging

logger = logging.getLogger(__name__)


def make_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_client(db: AsyncSession, client: ClientCreate):
    result = await db.execute(select(Client).filter_by(id=client.id))
    from_db_client = result.scalar_one_or_none()

    created_at = make_naive(client.created_at)
    date = datetime.fromisoformat(str(created_at)).date().isoformat()

    await store_daily_report(db, date=date, client=client)

    if from_db_client is not None:
        from_db_client.client_status = "regular"
        from_db_client.age = int((from_db_client.age + client.age) / 2)
        from_db_client.time = client.time
        db_client = from_db_client
    else:
        db_client = Client(**client.model_dump())
        db_client.client_status = "new"
        db_client.created_at = created_at

    try:
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error occurred while creating client: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred") from e

    return ClientResponse.model_validate(db_client)


async def store_daily_report(db: AsyncSession, date: str, client):
    result = await db.execute(select(DailyReport).filter_by(date=date))
    daily_report = result.scalar_one_or_none()

    if daily_report is None:
        daily_report = DailyReport(
            date=date,
            clients=[client.id],
            gender={client.gender: 1},
            age={client.age: 1},
            total_new_clients=1,
            total_regular_clients=0
        )
    else:
        daily_report.clients.append(client.id)

        if client.gender in daily_report.gender:
            daily_report.gender[client.gender] += 1
        else:
            daily_report.gender[client.gender] = 1

        if client.age in daily_report.age:
            daily_report.age[client.age] += 1
        else:
            daily_report.age[client.age] = 1

        if client.client_status == "new":
            daily_report.total_new_clients += 1
        else:
            daily_report.total_regular_clients += 1

    try:
        db.add(daily_report)
        await db.commit()
        await db.refresh(daily_report)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error occurred while storing daily report: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred on da") from e
