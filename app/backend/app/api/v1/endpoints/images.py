from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.schemas.image import Image as ImageSchema
from app.services.image_service import ImageService
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/", response_model=ImageSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        image = await ImageService.create_image(db, file)
        # Add URL to response
        image.url = f"{settings.BASE_URL}/uploads/images/{image.filepath}"
        return image
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ImageSchema])
def read_images(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    images = ImageService.get_images(db, skip=skip, limit=limit)
    for img in images:
        img.url = f"{settings.BASE_URL}/uploads/images/{img.filepath}"
    return images

@router.delete("/{image_id}", response_model=ImageSchema)
def delete_image(
    image_id: int, 
    db: Session = Depends(get_db)
):
    image = ImageService.delete_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image.url = f"{settings.BASE_URL}/uploads/images/{image.filepath}"
    return image
