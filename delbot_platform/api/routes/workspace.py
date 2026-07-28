from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from delbot_platform.research.models import ResearchResult
from delbot_platform.research.research_engine import ResearchEngine
from delbot_platform.workspace.session_manager import SessionManager


router = APIRouter(
    prefix="/api/workspace",
    tags=["Workspace"],
)

session_manager = SessionManager()

research_engine = ResearchEngine(
    session_manager=session_manager,
)


class CreateSessionRequest(BaseModel):

    title: str = "Untitled Research"


class AskRequest(BaseModel):

    query: str


@router.post("/session")
def create_session(
    body: CreateSessionRequest,
):

    return session_manager.create(
        body.title,
    )


@router.get("/sessions")
def sessions():

    return [
        session.export()
        for session in session_manager.sessions.values()
    ]


@router.get("/{session_id}")
def get_session(
    session_id: str,
):

    session = session_manager.get(
        session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return session


@router.post("/{session_id}/ask")
async def ask(
    session_id: str,
    body: AskRequest,
):

    session = session_manager.get(
        session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    result: ResearchResult = await research_engine.ask(
        session_id=session_id,
        query=body.query,
        history=session["messages"],
    )

    session_manager.add_message(
        session_id,
        "user",
        body.query,
    )

    session_manager.add_message(
        session_id,
        "assistant",
        result.answer,
    )

    updated = session_manager.get(
        session_id,
    )

    response = result.export()

    response["session_id"] = session_id
    response["messages"] = updated["messages"]

    return response
