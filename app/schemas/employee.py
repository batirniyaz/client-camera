import datetime

from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

# if TYPE_CHECKING:
from app.schemas.employee_image import EmployeeImageResponse
from app.schemas.position import PositionResponse
from app.schemas.working_graphic import WorkingGraphicResponse
from app.schemas.filial import FilialResponse


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
    name: str = Field(..., description="The name of the employee")
    position: 'PositionResponse' = Field(..., description="The position of the employee")
    filial: 'FilialResponse' = Field(..., description="The filial of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    working_graphic: 'WorkingGraphicResponse' = Field(None, description="The working graphic of the employee")
    images: list['EmployeeImageResponse'] = Field([], description="A list of images associated with the employee")

    created_at: datetime.datetime = Field(..., description="The time the employee was created")
    updated_at: datetime.datetime = Field(..., description="The time the employee was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Employee 1",
                "position": {
                    "id": 1,
                    "name": "Position 1",
                    "employees": 10,
                    "created_at": "2024-07-25 12:00:00"
                },
                "filial": {
                    "id": 1,
                    "name": "Filial 1",
                    "created_at": "2024-07-25 12:00:00"
                },
                "phone_number": "1234567890",
                "working_graphic": {
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
                },
                "images": [
                    {
                        "id": 1,
                        "url": "https://example.com/image.jpg",
                        "created_at": "2024-07-25 12:00:00"
                    }
                ],
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True
