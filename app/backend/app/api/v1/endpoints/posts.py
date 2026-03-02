from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.schemas.post import Post as PostSchema, PostCreate
from app.services.post_service import PostService

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def create_post(
    request: Request,
    post: PostCreate,
    db: Session = Depends(get_db)
):
    try:
        return PostService.create_post(db, post)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[PostSchema])
def read_posts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return PostService.get_posts(db, skip=skip, limit=limit)

@router.delete("/{post_id}", response_model=PostSchema)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db)
):
    post = PostService.delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
