import datetime

from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    id: int = Field(..., description="The ID of the client")
    gender: str = Field(..., description="Gender of the client")
    camera_id: int = Field(..., description="The ID of the camera")
    score: str = Field(..., description="The score of the client")
    age: int = Field(..., description="The age of the client")
    client_status: str = Field(..., description="The status of the client")
    time: str = Field(..., description="The time of the client")


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):

    created_at: datetime.datetime = Field(..., description="The time the client was created")
    updated_at: datetime.datetime = Field(..., description="The time the client was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "gender": "male",
                "camera_id": 1,
                "score": "0.8",
                "age": 22,
                "client_status": "new",
                "time": "12:00:00",
            }
        }
        arbitrary_types_allowed = True
