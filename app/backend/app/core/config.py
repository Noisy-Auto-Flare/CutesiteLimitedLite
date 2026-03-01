from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    APP_ENV: str = "production"
    APP_PORT: int = 8000
    DOMAIN: str = "localhost"
    BASE_URL: str = "http://localhost:8000"

    MAX_IMAGES: int = 50
    MAX_VIDEOS: int = 15
    MAX_POSTS: int = 50

    MAX_VIDEO_SIZE_MB: int = 100
    MAX_VIDEO_DURATION_SECONDS: int = 60
    MAX_POST_LENGTH: int = 10000

    UPLOAD_IMAGES_DIR: str = "uploads/images"
    UPLOAD_VIDEOS_DIR: str = "uploads/videos"

    DATABASE_URL: str = "sqlite:///./uploads/cutesite.db"
    
    SECRET_KEY: str = "supersecretkey"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra="ignore")

    @property
    def max_video_size_bytes(self):
        return self.MAX_VIDEO_SIZE_MB * 1024 * 1024

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_IMAGES_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_VIDEOS_DIR, exist_ok=True)
