from pydantic import BaseModel, Field
from typing import Optional, List


class EmployeeImageCreate(BaseModel):
    employee_id: int
    image_url: str


class EmployeeImageResponse(BaseModel):
    employee_id: int = Field(..., description="The ID of associated employee")
    image_id: int = Field(..., description="The ID of the image")
    image_url: str = Field(..., description="The URL of employee image")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "employee_id": 1,
                "image_id": 1,
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
