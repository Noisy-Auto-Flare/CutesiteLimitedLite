from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: Optional[str] = None
    content: str

class PostCreate(PostBase):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=10000)

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
