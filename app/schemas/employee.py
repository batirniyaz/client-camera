from pydantic import BaseModel
from typing import List


class EmployeeImageCreate(BaseModel):
    image_url: str


class EmployeeCreate(BaseModel):
    name: str
    phone_number: str
    position: str
    images: List[EmployeeImageCreate]


class EmployeeImageResponse(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class EmployeeResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    position: str
    images: List[EmployeeImageResponse]

    class Config:
        from_attributes = True
