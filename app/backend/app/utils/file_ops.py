import aiofiles
import os
import shutil
from typing import Optional
from fastapi import UploadFile, HTTPException

async def save_upload_file(upload_file: UploadFile, destination: str, max_size_bytes: Optional[int] = None) -> int:
    try:
        size = 0
        async with aiofiles.open(destination, 'wb') as out_file:
            while content := await upload_file.read(1024 * 1024):
                size += len(content)
                if max_size_bytes is not None and size > max_size_bytes:
                    await out_file.flush()
                    await out_file.close()
                    if os.path.exists(destination):
                        os.remove(destination)
                    raise HTTPException(status_code=413, detail="File too large")
                await out_file.write(content)
        return size
    except HTTPException:
        if os.path.exists(destination):
            os.remove(destination)
        raise
    except Exception as e:
        if os.path.exists(destination):
            os.remove(destination)
        raise HTTPException(status_code=500, detail="Could not save file")

def delete_file(filepath: str):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return True
        except OSError:
            return False
    return False
