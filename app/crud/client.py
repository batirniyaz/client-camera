from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, Union

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


async def store_daily_report(db: AsyncSession, date: str, client: ClientCreate):
    try:
        result = await db.execute(select(DailyReport).filter_by(date=date))
        daily_report = result.scalar_one_or_none()

        client_time = parse_datetime(client.time)
        rounded_time = client_time.replace(second=0, microsecond=0, minute=0, hour=client_time.hour) + timedelta(
            minutes=30 * round(client_time.minute / 30)
        )
        rounded_time_str = rounded_time.strftime("%H:%M")

        time_slot_data = defaultdict(lambda: {
            "time": rounded_time_str,
            "male_count": 0,
            "female_count": 0,
            "client_count": 0
        })

        if daily_report is None:
            daily_report = DailyReport(
                date=date,
                clients=[client.id],
                gender={client.gender: 1},
                age={str(client.age): 1},
                total_new_clients=1 if client.client_status == "new" else 0,
                total_regular_clients=1 if client.client_status == "regular" else 0,
                time_slots=[],
                male_percentage=0,
                female_percentage=0
            )

            if client.gender.lower() == "male":
                time_slot_data[rounded_time_str]["male_count"] += 1
            elif client.gender.lower() == "female":
                time_slot_data[rounded_time_str]["female_count"] += 1
            time_slot_data[rounded_time_str]["client_count"] += 1
            daily_report.time_slots.append(time_slot_data[rounded_time_str])
        else:
            if client.id not in daily_report.clients:
                if client.client_status == "new":
                    daily_report.total_new_clients += 1
                else:
                    daily_report.total_regular_clients += 1

                daily_report.clients = list(set(daily_report.clients + [client.id]))

                daily_report.gender[client.gender] = daily_report.gender.get(client.gender, 0) + 1

                age_key = str(client.age)
                daily_report.age[age_key] = daily_report.age.get(age_key, 0) + 1

                updated = False
                for slot in daily_report.time_slots:
                    if slot["time"] == rounded_time_str:
                        slot["client_count"] += 1
                        if client.gender.lower() == "male":
                            slot["male_count"] += 1
                        elif client.gender.lower() == "female":
                            slot["female_count"] += 1
                        updated = True
                        break

                if not updated:
                    if client.gender.lower() == "male":
                        time_slot_data[rounded_time_str]["male_count"] += 1
                    elif client.gender.lower() == "female":
                        time_slot_data[rounded_time_str]["female_count"] += 1
                    time_slot_data[rounded_time_str]["client_count"] += 1
                    daily_report.time_slots.append(time_slot_data[rounded_time_str])

            total_clients = len(daily_report.clients)
            male_count = daily_report.gender.get("male", 0)
            female_count = daily_report.gender.get("female", 0)

            if total_clients > 0:
                daily_report.male_percentage = (male_count / total_clients) * 100
                daily_report.female_percentage = (female_count / total_clients) * 100

            flag_modified(daily_report, "gender")
            flag_modified(daily_report, "age")
            flag_modified(daily_report, "time_slots")

        db.add(daily_report)
        await db.commit()
        await db.refresh(daily_report)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error occurred while storing daily report: {e}")
        raise HTTPException(status_code=400, detail="Integrity error occurred while storing daily report") from e


async def get_daily_report(
        db: AsyncSession,
        date: Optional[Union[str, datetime]] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None
):
    try:
        if date:
            date_str = date.strftime("%Y-%m-%d")
            res = await db.execute(select(DailyReport).filter_by(date=date_str))
            daily_report = res.scalar_one_or_none()
            return DailyReportResponse.model_validate(daily_report)

        start_date_str = start_datetime.date().isoformat()
        end_date_str = end_datetime.date().isoformat()

        query = select(DailyReport).filter(
            DailyReport.date.between(start_date_str, end_date_str)
        )
        res = await db.execute(query)
        reports = res.scalars().all()

        if not reports:
            raise HTTPException(status_code=404, detail="No reports found for the given date range.")

        combined_clients = set()
        combined_gender_counts = defaultdict(int)
        combined_age_counts = defaultdict(int)
        combined_time_slots = defaultdict(lambda: {"male_count": 0, "female_count": 0, "client_count": 0})

        for report in reports:
            report_date = datetime.strptime(report.date, "%Y-%m-%d")

            for client in report.clients:
                db_client = await db.execute(select(Client).filter_by(id=client))
                client = db_client.scalar_one_or_none()
                client_time = datetime.strptime(client.time[:16], "%Y-%m-%d %H:%M")

                if report_date == start_datetime.date():
                    if client_time >= start_datetime:
                        combined_clients.add(client.id)
                elif report_date == end_datetime.date():
                    if client_time <= end_datetime:
                        combined_clients.add(client.id)
                else:
                    combined_clients.add(client.id)

            for gender, count in report.gender.items():
                combined_gender_counts[gender] += count
            for age, count in report.age.items():
                combined_age_counts[age] += count
            for slot in report.time_slots:
                rounded_time = slot["time"]
                combined_time_slots[rounded_time]["client_count"] += slot["client_count"]
                combined_time_slots[rounded_time]["male_count"] += slot["male_count"]
                combined_time_slots[rounded_time]["female_count"] += slot["female_count"]

        total_new_clients = len(combined_clients)
        total_regular_clients = len(combined_clients)

        male_count = combined_gender_counts["male"]
        female_count = combined_gender_counts["female"]
        male_percentage = (male_count / total_new_clients) * 100 if total_new_clients > 0 else 0
        female_percentage = (female_count / total_new_clients) * 100 if total_new_clients > 0 else 0

        response_data = {
            "start_date": start_datetime.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_datetime.strftime("%Y-%m-%d %H:%M"),
            "clients": list(combined_clients),
            "gender": dict(combined_gender_counts),
            "age": dict(combined_age_counts),
            "time_slots": [
                {"time": time, **counts}
                for time, counts in sorted(combined_time_slots.items())
            ],
            "total_new_clients": total_new_clients,
            "total_regular_clients": total_regular_clients,
            "male_percentage": male_percentage,
            "female_percentage": female_percentage,
        }
        return response_data

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving data: {e}")


def round_time_slot(time):
    if time.minute >= 30:
        rounded_hour = (time.hour + 1) % 24
        rounded_minute = 0
    else:
        rounded_hour = time.hour
        rounded_minute = 30

    return f"{rounded_hour:02}:{rounded_minute:02}"
