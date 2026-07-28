from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.research.research_engine import ResearchEngine
from delbot_platform.workspace.session_manager import SessionManager


router = APIRouter(
    prefix="/api/research",
    tags=["Research"],
)

session_manager = SessionManager()

engine = ResearchEngine(
    session_manager=session_manager,
)


class ResearchRequest(BaseModel):

    session_id: str

    query: str


@router.post("/ask")
async def ask_research(
    request: ResearchRequest,
):

    result = await engine.ask(
        session_id=request.session_id,
        query=request.query,
    )

    return {
        "session_id": request.session_id,
        "query": request.query,
        "answer": result.answer,
        "sources": result.sources,
        "research_state": result.research_state,
    }
