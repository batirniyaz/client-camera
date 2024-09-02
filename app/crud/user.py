from sqlalchemy.ext.asyncio import AsyncSession

sms = []


async def send_sms(db: AsyncSession, sender_number: str, sender_message: str):
    data = {"sender_number": sender_number, "sender_message": sender_message}
    sms.append(data)
    return {"message": "SMS stored successfully"}


async def get_sms():
    return sms
