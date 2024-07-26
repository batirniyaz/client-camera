from pydantic import BaseModel, Field
from typing import List, Optional
from .employee_image import EmployeeImageResponse


class EmployeeCreate(BaseModel):
    name: str = Field(..., description="The name of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    position_id: int = Field(..., description="The ID of the employee's position")
    filial_id: int = Field(..., description="The ID of the filial")
    time_in: str = Field(..., description="The time the employee checks in")
    time_out: str = Field(..., description="The time the employee checks out")


class EmployeeResponse(BaseModel):
    id: int = Field(..., description="The ID of the employee")
    name: str = Field(..., description="The name of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    position_id: int = Field(..., description="The ID of the position")
    filial_id: int = Field(..., description="The ID of the filial")
    time_in: str = Field(..., description="The time the employee checks in")
    time_out: str = Field(..., description="The time the employee checks out")
    images: List[EmployeeImageResponse] = Field(..., description="A list of images associated with the employee")

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


class EmployeeUpdate(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    position_id: Optional[int]
    filial_id: Optional[int]
    time_in: Optional[str]
    time_out: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Batirniyaz",
                "phone_number": "998905913873",
                "position_id": 1,
                "filial_id": 1,
                "time_in": "09:00",
                "time_out": "19:00"
            }
        }
