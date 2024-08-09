import datetime

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from .employee_image import EmployeeImageResponse


class EmployeeBase(BaseModel):
    name: str = Field(..., description="The name of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    position_id: int = Field(..., description="The ID of the employee's position")
    working_graphic_id: Optional[int] = Field(None, description="The ID of the employee's working graphic")
    filial_id: int = Field(..., description="The ID of the filial")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = Field(None, description="The name of the employee")
    phone_number: Optional[str] = Field(None, description="The phone number of the employee")
    position_id: Optional[int] = Field(None, description="The ID of the employee's position")
    working_graphic_id: Optional[int] = Field(None, description="The ID of the employee's working graphic")
    filial_id: Optional[int] = Field(None, description="The ID of the filial")

    class Config:
        validate_assignment = True


class EmployeeResponse(EmployeeBase):
    id: int = Field(..., description="The ID of the employee")
    images: list[EmployeeImageResponse] = Field([], description="A list of images associated with the employee")

    created_at: datetime.datetime = Field(..., description="The time the employee was created")
    updated_at: datetime.datetime = Field(..., description="The time the employee was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Batirniyaz",
                "phone_number": "998905913873",
                "position_id": 1,
                "filial_id": 1,
                "images": [
                    {
                        "employee_id": 1,
                        "image_url": "http://example.com/image.jpg"
                    }
                ]
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True

        # @model_validator
        # def number_validator(cls, values):
        #     dt = datetime.datetime.now()
        #     if values["created_at"] is None:
        #         values["created_at"] = dt
        #     values["updated_at"] = dt
        #     return values
