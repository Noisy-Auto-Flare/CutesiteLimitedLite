import aiofiles
import os
import shutil
from fastapi import UploadFile, HTTPException

async def save_upload_file(upload_file: UploadFile, destination: str) -> int:
    try:
        size = 0
        async with aiofiles.open(destination, 'wb') as out_file:
            while content := await upload_file.read(1024 * 1024):  # Read 1MB chunks
                await out_file.write(content)
                size += len(content)
        return size
    except Exception as e:
        # Clean up if error
        if os.path.exists(destination):
            os.remove(destination)
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

def delete_file(filepath: str):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return True
        except OSError:
            return False
    return False
