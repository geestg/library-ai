from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.research.research_engine import (
    ResearchEngine,
)
from delbot_platform.workspace.session_manager import (
    SessionManager,
)


router = APIRouter(
    prefix="/v1/research",
    tags=["Research"],
)

session_manager = SessionManager()

engine = ResearchEngine(
    session_manager=session_manager,
)


class ResearchRequest(BaseModel):

    session_id: str

    query: str


@router.post("/chat")
async def research_chat(
    body: ResearchRequest,
):

    result = await engine.ask(
        session_id=body.session_id,
        query=body.query,
    )

    return result
