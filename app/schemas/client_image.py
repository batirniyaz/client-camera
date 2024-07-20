from pydantic import BaseModel


class ClientImageCreate(BaseModel):
    image_url: str


class ClientImageResponse(BaseModel):
    id: int
    image_url: str

    class Config:
        orm_mode = True
