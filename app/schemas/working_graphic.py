from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DayBase(BaseModel):
    day: str = Field(..., description="The name of the day")
    time_in: Optional[str] = Field(None, description="The time the employee starts work")
    time_out: Optional[str] = Field(None, description="The time the employee finishes work")
    is_work_day: bool = Field(..., description="Whether the day is a work day")


class DayCreate(DayBase):
    pass


class DayUpdate(DayBase):
    day: Optional[str] = Field(None, description="The name of the day")
    time_in: Optional[str] = Field(None, description="The time the employee starts work")
    time_out: Optional[str] = Field(None, description="The time the employee finishes work")
    is_work_day: Optional[bool] = Field(None, description="Whether the day is a work day")


class DayResponse(DayBase):
    id: int = Field(..., description="The ID of the day")

    created_at: datetime = Field(..., description="The date and time the day was created")
    updated_at: datetime = Field(..., description="The date and time the day was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "day": "Monday",
                "time_in": "08:00:00",
                "time_out": "17:00:00",
                "is_work_day": True,
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True


class WorkingGraphicBase(BaseModel):
    name: str = Field(..., description="The name of the working graphic")


class WorkingGraphicCreate(WorkingGraphicBase):
    pass


class WorkingGraphicUpdate(WorkingGraphicBase):
    name: Optional[str] = Field(None, description="The name of the working graphic")


class WorkingGraphicResponse(WorkingGraphicBase):
    id: int = Field(..., description="The ID of the working graphic")
    days: List[DayResponse] = Field([], description="The days in the working graphic")
    employees: list[dict] = Field([], description="A list of employees with this working graphic")

    created_at: datetime = Field(..., description="The date and time the working graphic was created")
    updated_at: datetime = Field(..., description="The date and time the working graphic was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Working Graphic 1",
                "days": [
                    {
                        "id": 1,
                        "day": "Monday",
                        "time_in": "08:00:00",
                        "time_out": "17:00:00",
                        "is_work_day": True,
                        "created_at": "2024-07-25 12:00:00"
                    }
                ],
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True