from datetime import datetime

from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.future import select
from ..models import Client, DailyReport
from ..schemas import ClientResponse, ClientCreate, DailyReportResponse, DailyReportCreate
import logging

logger = logging.getLogger(__name__)


def make_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_client(db: AsyncSession, client: ClientCreate, background_tasks: BackgroundTasks):
    result = await db.execute(select(Client).filter_by(id=client.id))
    from_db_client = result.scalar_one_or_none()

    created_at = make_naive(client.created_at)
    date = datetime.fromisoformat(str(created_at)).date().isoformat()

    background_tasks.add_task(store_daily_report, db, date, client)

    # await store_daily_report(db, date=date, client=client)

    if from_db_client is not None:
        from_db_client.client_status = "regular"
        from_db_client.age = (from_db_client.age + client.age) // 2
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
    try:
        result = await db.execute(select(DailyReport).filter_by(date=date))
        daily_report = result.scalar_one_or_none()

        if daily_report is None:
            daily_report = DailyReport(
                date=date,
                clients=[client.id],
                gender={client.gender: 1},
                age={str(client.age): 1},
                total_new_clients=1 if client.client_status == "new" else 0,
                total_regular_clients=1 if client.client_status == "regular" else 0,
            )
        else:
            print(f"Before update: {daily_report.gender=}, {daily_report.age=}, {daily_report.clients=}")

            daily_report.clients = list(set(daily_report.clients + [client.id]))

            if daily_report.gender is None:
                daily_report.gender = {}
            daily_report.gender[client.gender] = daily_report.gender.get(client.gender, 0) + 1

            if daily_report.age is None:
                daily_report.age = {}
            age_key = str(client.age)
            daily_report.age[age_key] = daily_report.age.get(age_key, 0) + 1

            if client.client_status == "new":
                daily_report.total_new_clients += 1
            else:
                daily_report.total_regular_clients += 1

            flag_modified(daily_report, "gender")
            flag_modified(daily_report, "age")

            print(f"After update: {daily_report.gender=}, {daily_report.age=}, {daily_report.clients=}")

        db.add(daily_report)
        await db.commit()
        await db.refresh(daily_report)
        print(f"After commit: {daily_report.gender=}, {daily_report.age=}, {daily_report.clients=}")

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error occurred while storing daily report: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred on da") from e
