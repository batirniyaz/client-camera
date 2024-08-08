from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from .employee import EmployeeResponse


class WorkingGraphicBase(BaseModel):
    name: str = Field(..., description="The name of the working graphic")
    monday: str = Field(..., description="The working hours on Monday")
    tuesday: str = Field(..., description="The working hours on Tuesday")
    wednesday: str = Field(..., description="The working hours on Wednesday")
    thursday: str = Field(..., description="The working hours on Thursday")
    friday: str = Field(..., description="The working hours on Friday")
    saturday: str = Field(..., description="The working hours on Saturday")
    sunday: str = Field(..., description="The working hours on Sunday")


class WorkingGraphicCreate(WorkingGraphicBase):
    pass


class WorkingGraphicUpdate(WorkingGraphicBase):
    name: Optional[str] = Field(None, description="The name of the working graphic")
    monday: Optional[str] = Field(None, description="The working hours on Monday")
    tuesday: Optional[str] = Field(None, description="The working hours on Tuesday")
    wednesday: Optional[str] = Field(None, description="The working hours on Wednesday")
    thursday: Optional[str] = Field(None, description="The working hours on Thursday")
    friday: Optional[str] = Field(None, description="The working hours on Friday")
    saturday: Optional[str] = Field(None, description="The working hours on Saturday")
    sunday: Optional[str] = Field(None, description="The working hours on Sunday")


class WorkingGraphicResponse(WorkingGraphicBase):
    id: int
    employees: list[EmployeeResponse] = Field([], description="The number of employees in the working graphic")

    created_at: datetime.datetime = Field(..., description="The date and time the working graphic was created")
    updated_at: datetime.datetime = Field(..., description="The date and time the working graphic was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Working Graphic 1",
                "monday": "09:00 - 19:00",
                "tuesday": "09:00 - 19:00",
                "wednesday": "09:00 - 19:00",
                "thursday": "09:00 - 19:00",
                "friday": "09:00 - 19:00",
                "saturday": "09:00 - 19:00",
                "sunday": "09:00 - 19:00",
                "employees": 10,
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
