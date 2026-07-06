from fastapi import APIRouter
from fastapi import HTTPException

from app.services.research.session import (
    session_manager,
)


router = APIRouter(
    prefix="/session",
    tags=[
        "session",
    ],
)


# =========================================
# CREATE SESSION
# =========================================

@router.post("/create")
def create_session():

    session = (
        session_manager.create()
    )

    return session.to_dict()


# =========================================
# GET SESSION
# =========================================

@router.get("/{session_id}")
def get_session(
    session_id: str,
):

    session = (
        session_manager.get(
            session_id
        )
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail=(
                "Session not found."
            ),

        )

    return session.to_dict()


# =========================================
# DELETE DOCUMENT
# =========================================

@router.delete(
    "/{session_id}/documents/{document_id}"
)
def delete_document(

    session_id: str,

    document_id: str,

):

    # =====================================
    # RESOLVE SESSION
    # =====================================

    session = (
        session_manager.get(
            session_id
        )
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail=(
                "Session not found."
            ),

        )

    # =====================================
    # RESOLVE OWNED DOCUMENT
    # =====================================

    document = (
        session.documents.get_document(
            document_id
        )
    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail=(
                "Document not found."
            ),

        )

    # =====================================
    # REMOVE DOCUMENT
    # =====================================

    session.documents.remove_document(
        document_id
    )

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "status":
            "success",

        "session_id":
            session_id,

        "document_id":
            document_id,

        "message":
            "Document deleted successfully.",

    }


# =========================================
# DELETE SESSION
# =========================================

@router.delete("/{session_id}")
def delete_session(
    session_id: str,
):

    deleted = (
        session_manager.delete(
            session_id
        )
    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail=(
                "Session not found."
            ),

        )

    return {

        "status":
            "success",

        "session_id":
            session_id,

        "message":
            "Session deleted successfully.",

    }