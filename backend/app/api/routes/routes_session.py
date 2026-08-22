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
# LIST SESSION HISTORY
# =========================================
@router.get("/history")
def list_session_history():
    return session_manager.list_sessions_summary()


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