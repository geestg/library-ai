from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from uuid import uuid4

import os

from app.document.file_classifier import (
    classify_file
)

from app.rag.ingest import (
    ingest_pdf
)

from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
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

    with open(
        file_path,
        "wb"
    ) as f:

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
    # INGEST DOCUMENT
    # =================================

    ingest_result = ingest_pdf(

        pdf_path=file_path,

        title=file.filename,

        author="Unknown",

        year="2026"
    )

    # =================================
    # CREATE SESSION DOCUMENT
    # =================================

    document_id = str(
        uuid4()
    )

    ACTIVE_DOCUMENTS[
        document_id
    ] = {

        "document_id":
        document_id,

        "filename":
        file.filename,

        "file_type":
        file_type,

        "content":
        ingest_result[
            "full_text"
        ],

        "pages":
        ingest_result[
            "pages"
        ],

        "chunks":
        ingest_result[
            "chunks"
        ]
    }

    print(
        f"[SESSION DOCUMENT] "
        f"{file.filename}"
    )

    print(
        f"Document ID: "
        f"{document_id}"
    )

    print(
        f"Pages: "
        f"{ingest_result['pages']}"
    )

    print(
        f"Chunks: "
        f"{ingest_result['chunks']}"
    )

    # =================================
    # RESPONSE
    # =================================

    return {

        "status":
        "success",

        "document_id":
        document_id,

        "filename":
        file.filename,

        "file_type":
        file_type,

        "pages":
        ingest_result[
            "pages"
        ],

        "chunks":
        ingest_result[
            "chunks"
        ],

        "message":
        "Document uploaded successfully"
    }