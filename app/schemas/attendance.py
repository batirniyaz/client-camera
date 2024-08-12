import datetime

from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional


class AttendanceBase(BaseModel):
    person_id: int = Field(..., description="The ID of the employee")
    camera_id: int = Field(..., description="The ID of the device")
    time: str = Field(..., description="The time of the attendance")
    score: str = Field(..., description="The score of the attendance")


class AttendanceCreate(AttendanceBase):
    file: UploadFile = File(..., description="The image file to upload")


class AttendanceUpdate(AttendanceBase):
    person_id: Optional[int] = Field(None, description="The ID of the employee")
    camera_id: Optional[int] = Field(None, description="The ID of the device")
    time: Optional[str] = Field(None, description="The time of the attendance")
    score: Optional[str] = Field(None, description="The score of the attendance")


class AttendanceResponse(AttendanceBase):
    id: int = Field(..., description="The ID of the attendance")
    file_path: str = Field(..., description="The path to the attendance image")
    created_at: datetime.datetime = Field(..., description="The time the attendance was created")
    updated_at: datetime.datetime = Field(..., description="The time the attendance was updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "person_id": 1,
                "camera_id": 1,
                "time": "2021-08-01T12:00:00",
                "score": "0.98",
                "file_path": "http://example.com/image.jpg",
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00"
            }
        }
        arbitrary_types_allowed = True
        validate_assignment = True


