import datetime

from pydantic import BaseModel, Field
from typing import Optional, List


class EmployeeImageBase(BaseModel):
    image_url: str = Field(..., description="The URL of the image")
    employee_id: int = Field(..., description="The ID of the employee")
    device_id: Optional[int] = Field(0, description="The ID of the device")


class EmployeeImageCreate(EmployeeImageBase):
    pass


class EmployeeImageUpdate(EmployeeImageBase):
    pass



class EmployeeImageResponse(EmployeeImageBase):
    image_id: int = Field(..., description="The ID of the image")

    created_at: datetime = Field(..., description="The time the image was created")
    updated_at: datetime = Field(..., description="The time the image was updated")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "employee_id": 1,
                "image_id": 1,
                "image_url": "http://example.com/image.jpg",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }
