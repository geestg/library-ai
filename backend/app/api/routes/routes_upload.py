from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from uuid import uuid4
import os

from app.document.file_classifier import classify_file
from app.rag.ingest import ingest_pdf
from app.services.document.session_store import ACTIVE_DOCUMENTS

router = APIRouter()

# =====================================
# CONFIG
# =====================================

UPLOAD_DIR = "/tmp/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# =====================================
# UPLOAD DOCUMENT
# =====================================

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_type = classify_file(file.filename)

    ingest_result = ingest_pdf(
        pdf_path=file_path,
        title=file.filename,
        author="Unknown",
        year="2026"
    )

    document_id = str(uuid4())

    ACTIVE_DOCUMENTS[document_id] = {
        "document_id": document_id,
        "filename": file.filename,
        "file_type": file_type,
        "content": ingest_result.get("full_text", ""),
        "pages": ingest_result.get("pages", 0),
        "chunks": ingest_result.get("chunks", 0),
        "pages_data": ingest_result.get("pages_data", [])
    }

    print(f"[SESSION DOCUMENT] {file.filename}")
    print(f"Document ID: {document_id}")
    print(f"Pages: {ingest_result.get('pages', 0)}")
    print(f"Chunks: {ingest_result.get('chunks', 0)}")

    return {
        "status": "success",
        "document_id": document_id,
        "filename": file.filename,
        "file_type": file_type,
        "pages": ingest_result.get("pages", 0),
        "chunks": ingest_result.get("chunks", 0),
        "message": "Document uploaded successfully"
    }

# =====================================
# UPLOAD IMAGE
# =====================================

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/bmp"
}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload image and return URL for preview"""
    
    # Check file type
    content_type = file.content_type
    if content_type not in ALLOWED_IMAGE_TYPES:
        return {
            "status": "error",
            "message": f"File type {content_type} not allowed. Allowed: jpeg, png, gif, webp, bmp"
        }
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1] or ".jpg"
    unique_filename = f"{uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Return URL for preview
    image_url = f"/uploads/{unique_filename}"
    
    print(f"[IMAGE UPLOAD] {file.filename} -> {unique_filename}")
    
    return {
        "status": "success",
        "filename": unique_filename,
        "original_filename": file.filename,
        "url": image_url,
        "content_type": content_type,
        "message": "Image uploaded successfully"
    }

# =====================================
# LIST UPLOADED FILES
# =====================================

@router.get("/uploads")
async def list_uploads():
    """List all uploaded files"""
    files = []
    if os.path.exists(UPLOAD_DIR):
        for f in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, f)
            if os.path.isfile(file_path):
                files.append({
                    "filename": f,
                    "url": f"/uploads/{f}",
                    "size": os.path.getsize(file_path)
                })
    return {"files": files}