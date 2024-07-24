from pydantic import BaseModel, Field
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


class EmployeeImageResponse(BaseModel):
    employee_id: int = Field(..., description="The ID of associated employee")
    image_url: str = Field(..., description="The URL of employee image")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "employee_id": 1,
                "image_url": "http://example.com/image.jpg"
            }
        }


class EmployeeImageResponseModel(BaseModel):
    status: str = Field(..., description="The status of the response")
    message: str = Field(..., description="The message of the response")
    data: EmployeeImageResponse = Field(..., description="The data payload containing the employee information")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Image created successfully",
                "data": {
                    "employee_id": 1,
                    "image_url": "http://example.com/image.jpg"
                }
            }
        }



class EmployeeResponse(BaseModel):
    id: int = Field(..., description="The ID of the employee")
    name: str = Field(..., description="The name of the employee")
    phone_number: str = Field(..., description="The phone number of the employee")
    position_id: int = Field(..., description="The ID of the position")
    filial_id: int = Field(..., description="The ID of the filial")
    time_in: str = Field(..., description="The time the employee checks in")
    time_out: str = Field(..., description="The time the employee checks out")
    images: List[EmployeeImageResponse] = Field(..., description="A list of images associated with the employee")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Batirniyaz",
                "phone_number": "998905913873",
                "position_id": 1,
                "filial_id": 1,
                "time_in": "09:00",
                "time_out": "19:00",
                "images": [
                    {
                        "employee_id": 1,
                        "image_url": "http://example.com/image.jpg"
                    }
                ]
            }
        }

