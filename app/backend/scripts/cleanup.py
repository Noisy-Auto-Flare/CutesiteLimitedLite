import sys
import os
# Add parent dir to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.image import Image
from app.models.video import Video
from app.models.post import Post
from app.core.config import settings
from app.utils.file_ops import delete_file

def cleanup():
    db = SessionLocal()
    print("Starting cleanup...")

    # Images
    count_images = db.query(Image).count()
    if count_images > settings.MAX_IMAGES:
        print(f"Cleaning images: {count_images} > {settings.MAX_IMAGES}")
        excess = count_images - settings.MAX_IMAGES
        oldest = db.query(Image).order_by(Image.created_at.asc()).limit(excess).all()
        for img in oldest:
            path = os.path.join(settings.UPLOAD_IMAGES_DIR, img.filepath)
            if delete_file(path):
                print(f"Deleted file: {path}")
            else:
                print(f"Failed to delete file or not found: {path}")
            db.delete(img)
        db.commit()
    
    # Videos
    count_videos = db.query(Video).count()
    if count_videos > settings.MAX_VIDEOS:
        print(f"Cleaning videos: {count_videos} > {settings.MAX_VIDEOS}")
        excess = count_videos - settings.MAX_VIDEOS
        oldest = db.query(Video).order_by(Video.created_at.asc()).limit(excess).all()
        for vid in oldest:
            path = os.path.join(settings.UPLOAD_VIDEOS_DIR, vid.filepath)
            delete_file(path)
            db.delete(vid)
        db.commit()

    # Posts
    count_posts = db.query(Post).count()
    if count_posts > settings.MAX_POSTS:
        print(f"Cleaning posts: {count_posts} > {settings.MAX_POSTS}")
        excess = count_posts - settings.MAX_POSTS
        oldest = db.query(Post).order_by(Post.created_at.asc()).limit(excess).all()
        for p in oldest:
            db.delete(p)
        db.commit()

    print("Cleanup finished.")
    db.close()

if __name__ == "__main__":
    cleanup()
