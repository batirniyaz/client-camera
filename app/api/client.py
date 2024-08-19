from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.client import create_client, get_daily_report, make_naive, store_daily_report
from ..schemas import ClientCreate, ClientResponse
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=ClientResponse)
async def create_client_endpoint(background_tasks: BackgroundTasks, client: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
        Create a new client with the given details.

        - **id**: The ID of the client
        - **name**: The name of the client
        - **age**: The age of the client
        - **score**: The score of the client
        """

    created_client = await create_client(db, client, background_tasks)
    return created_client


@router.get("{date}")
async def get_daily_report_endpoint(date: str, db: AsyncSession = Depends(get_db)):
    """
    Get the daily report for the given date.
    :param date:
    :param db:
    :return:
    """
    return await get_daily_report(db, date)
