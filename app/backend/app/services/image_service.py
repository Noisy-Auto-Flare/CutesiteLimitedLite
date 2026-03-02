import os
import magic
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from app.models.image import Image
from app.core.config import settings
from app.utils.file_ops import save_upload_file, delete_file

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/heic",
    "image/heif",
    "image/heic-sequence",
    "image/heif-sequence",
    "image/avif",
    "image/bmp",
    "image/tiff"
]

class ImageService:
    @staticmethod
    async def create_image(db: Session, file: UploadFile):
        # 1. Validate MIME type
        # Read first 2048 bytes to detect mime
        header = await file.read(2048)
        mime = magic.from_buffer(header, mime=True)
        await file.seek(0) # Reset cursor

        if mime not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type: {mime}. Allowed: {ALLOWED_MIME_TYPES}"
            )
        
        # 2. Generate unique filename
        file_ext = file.filename.split(".")[-1] if "." in file.filename else ""
        if not file_ext:
             # Try to guess extension from mime
             file_ext = mime.split("/")[-1]
        
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        filepath = os.path.join(settings.UPLOAD_IMAGES_DIR, unique_filename)

        # 3. Save file
        size = await save_upload_file(file, filepath)

        # 4. Save to DB
        db_image = Image(
            filename=file.filename, # Original name
            filepath=unique_filename, # Stored name
            mimetype=mime,
            size=size
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        # 5. Enforce Limit (Delete oldest if count > MAX)
        # We do this after adding to ensure we have the new one.
        # Check count
        count = db.query(Image).count()
        if count > settings.MAX_IMAGES:
            excess = count - settings.MAX_IMAGES
            # Get oldest images to delete
            oldest_images = db.query(Image).order_by(Image.created_at.asc()).limit(excess).all()
            for img in oldest_images:
                # Delete file
                full_path = os.path.join(settings.UPLOAD_IMAGES_DIR, img.filepath)
                delete_file(full_path)
                # Delete from DB
                db.delete(img)
            db.commit()

        return db_image

    @staticmethod
    def get_images(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Image).order_by(Image.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_image(db: Session, image_id: int):
        return db.query(Image).filter(Image.id == image_id).first()

    @staticmethod
    def delete_image(db: Session, image_id: int):
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            return None
        
        full_path = os.path.join(settings.UPLOAD_IMAGES_DIR, image.filepath)
        delete_file(full_path)
        
        db.delete(image)
        db.commit()
        return image
