import datetime

from pydantic import BaseModel, Field
from typing import List, Optional
from .employee_image import EmployeeImageResponse


class EmployeeBase(BaseModel):
    name: str = Field(..., description="The name of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    time_in: Optional[str] = Field(..., description="The time the employee checks in")
    time_out: Optional[str] = Field(..., description="The time the employee checks out")
    position_id: int = Field(..., description="The ID of the employee's position")
    working_graphic_id: int = Field(..., description="The ID of the employee's working graphic")
    filial_id: int = Field(..., description="The ID of the filial")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = Field(None, description="The name of the employee")
    phone_number: Optional[str] = Field(None, description="The phone number of the employee")
    time_in: Optional[str] = Field(None, description="The time the employee checks in")
    time_out: Optional[str] = Field(None, description="The time the employee checks out")
    position_id: Optional[int] = Field(None, description="The ID of the employee's position")
    working_graphic_id: Optional[int] = Field(None, description="The ID of the employee's working graphic")
    filial_id: Optional[int] = Field(None, description="The ID of the filial")


class EmployeeResponse(EmployeeBase):
    id: int = Field(..., description="The ID of the employee")
    images: List[EmployeeImageResponse] = Field(..., description="A list of images associated with the employee")

    created_at: datetime = Field(..., description="The time the employee was created")
    updated_at: datetime = Field(..., description="The time the employee was updated")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Batirniyaz",
                "phone_number": "998905913873",
                "position_id": 1,
                "filial_id": 1,
                "time_in": "09:00",
                "time_out": "19:00",
                "images": [
                    {
                        "employee_id": 1,
                        "image_url": "http://example.com/image.jpg"
                    }
                ]
            }
        }

