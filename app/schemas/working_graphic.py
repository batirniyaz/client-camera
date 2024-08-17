from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
import datetime

from ..models.working_graphic import Day
from .employee import EmployeeResponse


class DayBase(BaseModel):
    day: str = Field(..., description="The day of the week")
    time_in: str = Field(..., description="The time the employee starts working")
    time_out: str = Field(..., description="The time the employee finishes working")
    is_work_day: bool = Field(..., description="Whether the day is a work day")


class DayCreate(DayBase):
    pass


class DayUpdate(DayBase):
    pass


class DayResponse(DayBase):
    id: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "day": "Monday",
                "time_in": "09:00",
                "time_out": "19:00",
                "is_work_day": True,
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True


class WorkingGraphicBase(BaseModel):
    name: str = Field(..., description="The name of the working graphic")


class WorkingGraphicCreate(WorkingGraphicBase):
    days: List[DayCreate] = Field([], description="The days of the week the employee works")


class WorkingGraphicUpdate(WorkingGraphicBase):
    pass


class WorkingGraphicResponse(WorkingGraphicBase):
    id: int
    days: List[DayResponse] = Field([], description="The days of the week the employee works")

    created_at: datetime.datetime = Field(..., description="The date and time the working graphic was created")
    updated_at: datetime.datetime = Field(..., description="The date and time the working graphic was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Graphic 1",
                "days": [
                    {
                        "id": 1,
                        "day": "Monday",
                        "time_in": "09:00",
                        "time_out": "19:00",
                        "is_work_day": True,
                        "created_at": "2024-07-25 12:00:00"
                    }
                ],
                "created_at": "2024-07-25 12:00:00"
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
