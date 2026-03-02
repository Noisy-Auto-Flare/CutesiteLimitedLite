import os
import magic
import uuid
import shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from app.models.video import Video
from app.core.config import settings
from app.utils.file_ops import save_upload_file, delete_file
from moviepy.editor import VideoFileClip

ALLOWED_VIDEO_MIME_TYPES = [
    "video/mp4",
    "video/webm",
    "video/ogg",
    "video/quicktime",
    "video/x-m4v",
    "video/3gpp",
    "video/3gpp2",
    "video/x-msvideo",
    "video/avi",
    "video/x-matroska"
]

class VideoService:
    @staticmethod
    async def create_video(db: Session, file: UploadFile):
        # 1. Validate MIME type
        header = await file.read(2048)
        # Use python-magic to detect mime from bytes
        # Note: magic.from_buffer returns string like 'video/mp4'
        mime = magic.from_buffer(header, mime=True)
        await file.seek(0)

        if mime not in ALLOWED_VIDEO_MIME_TYPES:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid video type: {mime}. Allowed: {ALLOWED_VIDEO_MIME_TYPES}"
            )

        # 2. Check size (approximate from content-length header if available, but stream is safer)
        # We'll check size after saving to temp file to be sure, or during stream.
        # But for duration check we need full file.

        # Generate unique filename
        filename = file.filename or "unknown.mp4"
        file_ext = filename.split(".")[-1] if "." in filename else "mp4"
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        filepath = os.path.join(settings.UPLOAD_VIDEOS_DIR, unique_filename)

        # 3. Save file
        try:
            size = 0
            with open(filepath, "wb") as buffer:
                while content := await file.read(1024 * 1024): # 1MB chunks
                    size += len(content)
                    buffer.write(content)
                    if size > settings.max_video_size_bytes:
                         buffer.close()
                         os.remove(filepath)
                         raise HTTPException(
                             status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                             detail=f"Video exceeds maximum size of {settings.MAX_VIDEO_SIZE_MB}MB"
                         )
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e

        # 4. Check Duration
        try:
            clip = VideoFileClip(filepath)
            duration = clip.duration
            clip.close()
            if duration > settings.MAX_VIDEO_DURATION_SECONDS:
                os.remove(filepath)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Video exceeds maximum duration of {settings.MAX_VIDEO_DURATION_SECONDS} seconds"
                )
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=400, detail=f"Invalid video file: {str(e)}")

        # 5. Save to DB
        db_video = Video(
            filename=filename,
            filepath=unique_filename,
            mimetype=mime,
            size=size,
            duration=duration
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        # 6. Enforce Limit
        count = db.query(Video).count()
        if count > settings.MAX_VIDEOS:
            excess = count - settings.MAX_VIDEOS
            oldest = db.query(Video).order_by(Video.created_at.asc()).limit(excess).all()
            for vid in oldest:
                full_path = os.path.join(settings.UPLOAD_VIDEOS_DIR, vid.filepath)
                delete_file(full_path)
                db.delete(vid)
            db.commit()

        return db_video

    @staticmethod
    def get_videos(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Video).order_by(Video.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_video(db: Session, video_id: int):
        return db.query(Video).filter(Video.id == video_id).first()
    
    @staticmethod
    def delete_video(db: Session, video_id: int):
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return None
        
        full_path = os.path.join(settings.UPLOAD_VIDEOS_DIR, video.filepath)
        delete_file(full_path)
        
        db.delete(video)
        db.commit()
        return video
