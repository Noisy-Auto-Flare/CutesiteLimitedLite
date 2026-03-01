from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    duration = Column(Float, nullable=False) # in seconds
    size = Column(Integer, nullable=False) # in bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
