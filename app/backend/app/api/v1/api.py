from fastapi import APIRouter
from app.api.v1.endpoints import images, videos, posts

api_router = APIRouter()

api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
