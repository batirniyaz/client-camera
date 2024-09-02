from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from app.crud.user import send_sms, get_sms

router = APIRouter()


@router.post("/send_sms", response_model=[])
async def send_sms_endpoint(sender_number: str = Query(...), sender_message: str = Query(...),
                            db: AsyncSession = Depends(get_db)):
    """
    Send SMS to the user.
    :param sender_message:
    :param sender_number:
    :param db:
    :return:
    """
    return await send_sms(db, sender_number, sender_message)


@router.get("/sms", response_model=[])
async def get_sms_endpoint():
    """
    Get the list of SMS.
    :param db:
    :return:
    """
    return await get_sms()
