import datetime

from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional


class EmployeeImageBase(BaseModel):
    image_url: str = Field(..., description="The URL of the image")
    employee_id: int = Field(..., description="The ID of the employee")
    device_id: Optional[int] = Field(0, description="The ID of the device")


class EmployeeImageCreate(EmployeeImageBase):
    file: UploadFile = File(..., description="The image file to upload")


class EmployeeImageUpdate(EmployeeImageBase):
    pass


class EmployeeImageResponse(EmployeeImageBase):
    image_id: int = Field(..., description="The ID of the image")
    image_url: str = Field(..., description="The URL of the image")

    created_at: datetime.datetime = Field(..., description="The time the image was created")
    updated_at: datetime.datetime = Field(..., description="The time the image was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "image_id": 1,
                "image_url": "http://example.com/image.jpg",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }
        arbitrary_types_allowed = True
