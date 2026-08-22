from uuid import uuid4

import os

from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from app.document.document_classifier import (
    classify_file,
)

from app.rag.ingest import (
    ingest_pdf,
)

from app.services.research.session import (
    session_manager,
)

from app.services.research.session.models.document_session import (
    DocumentItem,
)
router = APIRouter()


# =====================================
# CONFIG
# =====================================
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


# =====================================
# UPLOAD DOCUMENT
# =====================================
@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    session_id: str = Form(default="chat_session"),
):

    # =================================
    # RESOLVE SESSION (AUTO-CREATE IF NOT EXISTS)
    # =================================
    session = session_manager.get_or_create(
        session_id
    )

    # =================================
    # SAVE FILE
    # =================================
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename,
    )

    with open(
        file_path,
        "wb",
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
        year="2026",
    )

    # =================================
    # DOCUMENT ID
    # =================================
    document_id = str(
        uuid4()
    )

    # =================================
    # BUILD DOCUMENT
    # =================================
    document = DocumentItem(
        document_id=document_id,
        filename=file.filename,
        file_type=file_type,
        content=ingest_result.get(
            "full_text",
            "",
        ),
        pages=ingest_result.get(
            "pages",
            0,
        ),
        chunks=ingest_result.get(
            "chunks",
            0,
        ),
        pages_data=ingest_result.get(
            "pages_data",
            [],
        ),
    )

    # =================================
    # STORE DOCUMENT
    # =================================
    session.documents.add_document(
        document
    )

    # =================================
    # DEBUG
    # =================================
    print()
    print("=" * 60)
    print("DOCUMENT UPLOAD")
    print("=" * 60)
    print(
        f"Filename    : {file.filename}"
    )
    print(
        f"Document ID : {document_id}"
    )
    print(
        f"Session ID  : {session.session_id}"
    )
    print(
        f"Pages       : {document.pages}"
    )
    print(
        f"Chunks      : {document.chunks}"
    )
    print(
        "Stored      : WorkspaceSession.documents"
    )
    print("=" * 60)

    # =================================
    # RESPONSE
    # =================================
    return {
        "status":
            "success",
        "document_id":
            document.document_id,
        "filename":
            document.filename,
        "file_type":
            document.file_type,
        "pages":
            document.pages,
        "chunks":
            document.chunks,
        "session_id":
            session.session_id,
        "message":
            "Document uploaded successfully",

    }