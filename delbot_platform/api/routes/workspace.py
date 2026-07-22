from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from delbot_platform.workspace.session_manager import SessionManager
from delbot_platform.research.research_engine import ResearchEngine


router = APIRouter(
    prefix="/api/workspace",
    tags=["Workspace"],
)


session_manager = SessionManager()
research_engine = ResearchEngine()


class CreateSessionRequest(BaseModel):
    title: str = "Untitled Research"


class AskRequest(BaseModel):
    query: str


@router.post("/session")
def create_session(
    body: CreateSessionRequest,
):

    return session_manager.create(
        body.title
    )


@router.get("/sessions")
def sessions():

    return list(
        session_manager.sessions.values()
    )


@router.get("/{session_id}")
def get_session(
    session_id: str,
):

    session = session_manager.get(
        session_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return session


@router.post("/{session_id}/ask")
def ask(
    session_id: str,
    body: AskRequest,
):

    session = session_manager.get(
        session_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    query = body.query

    history = session["messages"]

    result = research_engine.ask(
        session_id=session_id,
        query=query,
        history=history,
    )

    session_manager.add_message(
        session_id,
        "user",
        query,
    )

    session_manager.add_message(
        session_id,
        "assistant",
        result["answer"],
    )

    state = session_manager.get_state(
        session_id
    )

    if state is not None:

        state.update_question(query)

        state.update_answer(
            result["answer"]
        )

        for source in result.get(
            "sources",
            [],
        ):
            state.add_source(source)

        session_manager.replace_state(
            session_id,
            state,
        )

    return {
        "session_id": session_id,
        "answer": result["answer"],
        "sources": result.get(
            "sources",
            [],
        ),
        "messages": session_manager.get(
            session_id
        )["messages"],
        "research_state": session_manager.get(
            session_id
        )["research_state"],
    }