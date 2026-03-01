from pydantic import BaseModel
from datetime import datetime

class ImageBase(BaseModel):
    pass

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    filename: str
    mimetype: str
    size: int
    created_at: datetime
    url: str | None = None  # Computed field for frontend

    class Config:
        from_attributes = True
