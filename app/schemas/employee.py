from pydantic import BaseModel
from typing import List


class EmployeeCreate(BaseModel):
    name: str
    phone_number: str
    position_id: int
    filial_id: int
    time_in: str
    time_out: str


class EmployeeImageCreate(BaseModel):
    employee_id: int
    image_url: str
    device_id: int


class EmployeeImageResponse(BaseModel):
    employee_id: int
    image_url: str

    class Config:
        from_attributes = True


class EmployeeResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    position_id: int
    filial_id: int
    time_in: str
    time_out: str
    images: List[EmployeeImageResponse]

    class Config:
        from_attributes = True
