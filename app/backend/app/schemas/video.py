from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VideoBase(BaseModel):
    pass

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    filename: str
    mimetype: str
    size: int
    duration: float
    created_at: datetime
    url: Optional[str] = None

    class Config:
        from_attributes = True
