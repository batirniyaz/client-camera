from pydantic import BaseModel
from typing import List
from .client_image import ClientImageCreate, ClientImageResponse


class ClientCreate(BaseModel):
    person_id: int = None
    is_regular: str
    timestamp: str
    image_url: List[ClientImageCreate]


class ClientResponse(BaseModel):
    id: int
    person_id: int = None
    timestamp: str
    image_url: List[ClientImageResponse]

    class Config:
        orm_mode = True
