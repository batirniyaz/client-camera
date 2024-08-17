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

    created_at: datetime.datetime = Field(..., description="The time the client was created")


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
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


class DailyReportBase(BaseModel):
    date: str = Field(..., description="The date of the report")
    clients: list[int] = Field([], description="A list of clients")
    gender: dict[str, int] = Field({}, description="A dictionary for gender distribution")
    age: dict[int, int] = Field({}, description="A dictionary for age distribution")
    total_new_clients: int = Field(..., description="The total number of new clients")
    total_regular_clients: int = Field(..., description="The total number of regular clients")


class DailyReportCreate(DailyReportBase):
    pass


class DailyReportResponse(DailyReportBase):
    created_at: datetime.datetime = Field(..., description="The time the report was created")
    updated_at: datetime.datetime = Field(..., description="The time the report was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        json_schema_extra = {
            "example": {
                "date": "2021-01-01",
                "clients": [1, 2, 3],
                "gender": {"male": 4, "female": 2},
                "age": {20: 2, 25: 3, 30: 1},
                "total_new_clients": 4,
                "total_regular_clients": 2,
            }
        }
        arbitrary_types_allowed = True
