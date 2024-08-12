import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(EmailStr, description="The email of the user")
    phone_number: str = Field(..., description="The phone number of the user")


class UserCreate(UserBase):
    password: str = Field(..., description="The password of the user")


class UserUpdate(UserBase):
    name: Optional[str] = Field(None, description="The name of the user")
    email: Optional[EmailStr] = Field(None, description="The email of the user")
    phone_number: Optional[str] = Field(None, description="The phone number of the user")
    password: Optional[str] = Field(None, description="The password of the user")


class UserResponse(UserBase):
    id: int = Field(..., description="The ID of the user")
    created_at: datetime.datetime = Field(..., description="The time the user was created")
    updated_at: datetime.datetime = Field(..., description="The time the user was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Batirniyaz",
                "email": "batya@gmail.com,",
                "phone_number": "1234567890",
                "password": "password",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }
        arbitrary_types_allowed = True




