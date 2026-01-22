from fastapi import APIRouter, UploadFile, File
from fastapi import Form
import os
import aiofiles

router = APIRouter(prefix="/upload", tags=["File Upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
}

@router.post("/upload-chunk")
async def upload_chunk(
    chunk: UploadFile = File(...),
    filename: str = Form(...),
    chunkIndex: int = Form(...),
    totalChunks: int = Form(...),
):
    temp_path = f"uploads/{filename}.part{chunkIndex}"
    
    async with aiofiles.open(temp_path, "wb") as f:
        await f.write(await chunk.read())
    
    # If last chunk, combine all parts
    if chunkIndex == totalChunks - 1:
        final_path = f"uploads/{filename}"
        async with aiofiles.open(final_path, "wb") as final:
            for i in range(totalChunks):
                part_path = f"uploads/{filename}.part{i}"
                async with aiofiles.open(part_path, "rb") as part:
                    await final.write(await part.read())
                os.remove(part_path)
    
    return {"chunkIndex": chunkIndex, "received": True}