from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from app.core.config import settings

class PostService:
    @staticmethod
    def create_post(db: Session, post: PostCreate):
        # 1. Create DB record
        db_post = Post(
            title=post.title,
            content=post.content
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        # 2. Enforce Limit
        count = db.query(Post).count()
        if count > settings.MAX_POSTS:
            excess = count - settings.MAX_POSTS
            oldest = db.query(Post).order_by(Post.created_at.asc()).limit(excess).all()
            for p in oldest:
                db.delete(p)
            db.commit()

        return db_post

    @staticmethod
    def get_posts(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_post(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def delete_post(db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None
        db.delete(post)
        db.commit()
        return post
