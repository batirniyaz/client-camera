from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, BackgroundTasks
from sqlalchemy import Date, cast, TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.future import select

from .attendance import parse_datetime
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

    date = datetime.fromisoformat(str(client.time)).date().isoformat()
    print(f"{date=}")

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

    try:
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error occurred while creating client: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred") from e

    return ClientResponse.model_validate(db_client)


async def store_daily_report(
        db: AsyncSession,
        date: Optional[datetime] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None
):
    try:
        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            result = await db.execute(select(DailyReport)
                                      .where(cast(DailyReport.date, Date) == date_obj.date()))
            daily_reports = result.scalars().all()

            if daily_reports:
                for report in daily_reports:
                    await db.delete(report)
                await db.commit()
                print(f"Deleted existing DailyReports for date {date.date()}.")

            daily_report = DailyReport(
                date=str(date.date()),
                clients=[],
                gender={},
                age={},
                total_new_clients=0,
                total_regular_clients=0,
                time_slots=[],
                male_percentage=0.0,
                female_percentage=0.0,
            )
        else:
            daily_report = DailyReport(
                date=str(start_datetime.date()),
                clients=[],
                gender={},
                age={},
                total_new_clients=0,
                total_regular_clients=0,
                time_slots=[],
                male_percentage=0.0,
                female_percentage=0.0,
            )

        query = select(Client)
        if start_datetime and end_datetime:
            query = query.filter(
                cast(Client.time, TIMESTAMP) >= start_datetime,
                cast(Client.time, TIMESTAMP) <= end_datetime
            )
        elif start_datetime:
            query = query.filter(cast(Client.time, TIMESTAMP) >= start_datetime)
        elif end_datetime:
            query = query.filter(cast(Client.time, TIMESTAMP) <= end_datetime)
        elif date:
            day_start = date.replace(hour=0, minute=0, second=0)
            day_end = date.replace(hour=23, minute=59, second=59)
            query = query.filter(
                cast(Client.time, TIMESTAMP) >= day_start,
                cast(Client.time, TIMESTAMP) <= day_end
            )

        clients_result = await db.execute(query)
        clients = clients_result.scalars().all()

        time_slot_data = defaultdict(lambda: {
            "time": "",
            "male_count": 0,
            "female_count": 0,
            "client_count": 0
        })

        total_clients = 0
        total_males = 0
        total_females = 0

        for client in clients:
            if client.id not in daily_report.clients:
                if client.client_status == "new":
                    daily_report.total_new_clients += 1
                else:
                    daily_report.total_regular_clients += 1

                daily_report.clients.append(client.id)

                if client.gender in daily_report.gender:
                    daily_report.gender[client.gender] += 1
                else:
                    daily_report.gender[client.gender] = 1

                age_str = str(client.age)
                if age_str in daily_report.age:
                    daily_report.age[age_str] += 1
                else:
                    daily_report.age[age_str] = 1

                client_time = datetime.strptime(client.time, "%Y-%m-%d %H:%M:%S").time()
                rounded_time_slot = round_time_slot(client_time)

                if client.gender.lower() == "male":
                    total_males += 1
                elif client.gender.lower() == "female":
                    total_females += 1

                if rounded_time_slot not in time_slot_data:
                    time_slot_data[rounded_time_slot]["time"] = rounded_time_slot

                time_slot_data[rounded_time_slot]["client_count"] += 1

                if client.gender.lower() == "male":
                    time_slot_data[rounded_time_slot]["male_count"] += 1
                elif client.gender.lower() == "female":
                    time_slot_data[rounded_time_slot]["female_count"] += 1

            daily_report.time_slots = list(time_slot_data.values())
            total_clients = total_males + total_females

            if total_clients > 0:
                daily_report.male_percentage = (total_males / total_clients) * 100
                daily_report.female_percentage = (total_females / total_clients) * 100

        flag_modified(daily_report, "clients")
        flag_modified(daily_report, "gender")
        flag_modified(daily_report, "age")
        flag_modified(daily_report, "time_slots")

        print(f"After update: {daily_report.gender=}, {daily_report.age=}, {daily_report.clients=}")

        db.add(daily_report)
        await db.commit()
        await db.refresh(daily_report)
        print(
            f"After commit: {daily_report.gender=}, {daily_report.age=}, {daily_report.clients=}, {daily_report.time_slots=}")

        return DailyReportResponse.model_validate(daily_report).model_dump()

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error occurred while storing daily report: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred on da") from e


async def get_daily_report(db: AsyncSession, date: str):
    result = await db.execute(select(DailyReport).where(cast(DailyReport.date, Date) == date))
    daily_report = result.scalar_one_or_none()
    if not daily_report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return DailyReportResponse.model_validate(daily_report)


def round_time_slot(time):
    if time.minute >= 30:
        rounded_hour = (time.hour + 1) % 24
        rounded_minute = 0
    else:
        rounded_hour = time.hour
        rounded_minute = 30

    return f"{rounded_hour:02}:{rounded_minute:02}"
