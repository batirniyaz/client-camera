from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from .employee import EmployeeResponse


class PositionBase(BaseModel):
    name: str = Field(..., description="The name of the position")


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    name: Optional[str] = Field(None, description="The name of the position")


class PositionResponse(PositionBase):
    id: int = Field(..., description="The ID of the position")
    employees: List[EmployeeResponse] = Field([], description="The number of employees in the position")

    created_at: datetime.datetime = Field(..., description="The date and time the position was created")
    updated_at: datetime.datetime = Field(..., description="The date and time the position was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Position 1",
                "employees": 10,
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
