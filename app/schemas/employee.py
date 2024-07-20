from pydantic import BaseModel
from typing import List


class EmployeeImageCreate(BaseModel):
    image_url: str


class EmployeeCreate(BaseModel):
    person_id: int
    image_url: List[EmployeeImageCreate]


class EmployeeImageResponse(BaseModel):
    id: int
    image_url: str

    class Config:
        orm_mode = True


class EmployeeResponse(BaseModel):
    id: int
    person_id: int
    image_url: List[EmployeeImageResponse]

    class Config:
        orm_mode = True
