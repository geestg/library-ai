from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

from app.document.file_classifier import (
    classify_file
)

from app.rag.ingest import (
    ingest_pdf
)

router = APIRouter()

# =====================================
# CONFIG
# =====================================

UPLOAD_DIR = "/tmp/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# =====================================
# UPLOAD DOCUMENT
# =====================================

@router.post("/upload-pdf")
async def upload_pdf(

    file: UploadFile = File(...)
):

    # =================================
    # SAVE FILE
    # =================================

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:

        f.write(
            await file.read()
        )

    # =================================
    # FILE TYPE
    # =================================

    file_type = classify_file(
        file.filename
    )

    # =================================
    # INGEST PDF
    # =================================

    ingest_pdf(

        pdf_path=file_path,

        title=file.filename,

        author="Unknown",

        year="2026"
    )

    # =================================
    # RESPONSE
    # =================================

    return {

        "status": "success",

        "filename": file.filename,

        "file_type": file_type,

        "message": "PDF uploaded and indexed successfully"
    }