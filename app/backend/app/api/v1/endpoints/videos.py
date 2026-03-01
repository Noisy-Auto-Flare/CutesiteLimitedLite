from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.schemas.video import Video as VideoSchema
from app.services.video_service import VideoService
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/", response_model=VideoSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        video = await VideoService.create_video(db, file)
        video.url = f"{settings.BASE_URL}/uploads/videos/{video.filepath}"
        return video
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[VideoSchema])
def read_videos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    videos = VideoService.get_videos(db, skip=skip, limit=limit)
    for vid in videos:
        vid.url = f"{settings.BASE_URL}/uploads/videos/{vid.filepath}"
    return videos

@router.delete("/{video_id}", response_model=VideoSchema)
def delete_video(
    video_id: int, 
    db: Session = Depends(get_db)
):
    video = VideoService.delete_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.url = f"{settings.BASE_URL}/uploads/videos/{video.filepath}"
    return video
