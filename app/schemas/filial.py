from pydantic import BaseModel, Field
from typing import Optional


class FilialCreate(BaseModel):
    name: str
    address: str
    phone_number: str
    employees: int
    device_id: int
    created_at: Optional[str] = None


class FilialResponse(BaseModel):
    id: int = Field(..., description="The ID of the filial")
    name: str = Field(..., description="The name of the filial")
    address: str = Field(..., description="The address of the filial")
    employees: int = Field(..., description="The number of employees in the filial")
    device_id: int = Field(..., description="The ID of the device")
    created_at: str = Field(..., description="The date and time the filial was created")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Filial 1",
                "address": "123 dosnazarov",
                "employees": 10,
                "device_id": 1,
                "created_at": "2024-07-25 12:00:00"
            }
        }


class FilialResponseModel(BaseModel):
    status: str = Field(..., description="The status of the response")
    message: str = Field(..., description="The message of the response")
    data: FilialResponse = Field(..., description="The data payload containing the filial information")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Filial created successfully",
                "data": {
                    "id": 1,
                    "name": "Filial 1",
                    "address": "123 dosnazarov",
                    "employees": 10,
                    "device_id": 1,
                    "created_at": "2024-07-25 12:00:00"
                }
            }
        }
class FilialUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    employees: Optional[int]
    device_id: Optional[int]
    created_at: Optional[str] = None

