from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.schemas.video import Video as VideoSchema
from app.services.video_service import VideoService

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

def get_public_base_url(request: Request) -> str:
    base_url = str(request.base_url).rstrip("/")
    if base_url.endswith("/api/v1"):
        base_url = base_url[: -len("/api/v1")]
    return base_url

@router.post("/", response_model=VideoSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        video = await VideoService.create_video(db, file)
        base_url = get_public_base_url(request)
        video.url = f"{base_url}/uploads/videos/{video.filepath}"
        return video
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[VideoSchema])
def read_videos(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    videos = VideoService.get_videos(db, skip=skip, limit=limit)
    base_url = get_public_base_url(request)
    for vid in videos:
        vid.url = f"{base_url}/uploads/videos/{vid.filepath}"
    return videos

@router.delete("/{video_id}", response_model=VideoSchema)
def delete_video(
    request: Request,
    video_id: int, 
    db: Session = Depends(get_db)
):
    video = VideoService.delete_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    base_url = get_public_base_url(request)
    video.url = f"{base_url}/uploads/videos/{video.filepath}"
    return video
