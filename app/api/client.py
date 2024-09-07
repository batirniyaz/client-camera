from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import current_user
from app.auth.db import User
from ..crud.client import create_client, get_daily_report
from ..schemas import ClientCreate, ClientResponse
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=ClientResponse)
async def create_client_endpoint(
        background_tasks: BackgroundTasks,
        client: ClientCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(current_user)
):
    """
        Create a new client with the given details.

        - **id**: The ID of the client
        - **name**: The name of the client
        - **age**: The age of the client
        - **score**: The score of the client
        """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    created_client = await create_client(db, client, background_tasks)
    return created_client


@router.get("/reports", response_model=[])
async def get_daily_report_endpoint(
        date: Optional[str] = Query(None, alias="date", description="YYYY-MM-DD format"),
        db: AsyncSession = Depends(get_db),
        date1: Optional[str] = Query(None, alias="start_datetime", description="YYYY-MM-DD %H:%M format"),
        date2: Optional[str] = Query(None, alias="end_datetime", description="YYYY-MM-DD %H:%M format"),
        user: User = Depends(current_user)
):
    """
    Get the daily report for the given date.
    :param user:
    :param date2:
    :param date1:
    :param date:
    :param db:
    :return:
    """

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d") if date else None

        start_datetime = datetime.strptime(date1, "%Y-%m-%d %H:%M") if date1 else None
        end_datetime = datetime.strptime(date2, "%Y-%m-%d %H:%M") if date2 else None

        if not date and not (start_datetime and end_datetime):
            raise HTTPException(status_code=400,
                                detail="You must provide either a date or both start_datetime and end_datetime.")

        report = await get_daily_report(db=db, date=date_obj, start_datetime=start_datetime, end_datetime=end_datetime)
        return report

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
