from pydantic import BaseModel, Field
from typing import Optional, List
from .employee import EmployeeResponse

import datetime


class FilialBase(BaseModel):
    name: str = Field(..., description="The name of the filial")
    address: str = Field(..., description="The address of the filial")


class FilialCreate(FilialBase):
    pass


class FilialUpdate(FilialBase):
    name: Optional[str] = Field(None, description="The name of the filial")
    address: Optional[str] = Field(None, description="The address of the filial")


class FilialResponse(FilialBase):
    id: int = Field(..., description="The ID of the filial")
    employees: List[EmployeeResponse] = Field([], description="The number of employees in the filial")

    created_at: datetime.datetime = Field(..., description="The date and time the filial was created")
    updated_at: datetime.datetime = Field(..., description="The date and time the filial was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Filial 1",
                "address": "123 dosnazarov",
                "employees": 10,
                "device_id": 1,
                "created_at": "2024-07-25 12:00:00"
            }
        }
        arbitrary_types_allowed = True
