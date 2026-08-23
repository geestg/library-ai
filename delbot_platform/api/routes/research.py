from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from delbot_platform.research.models import Citation, ResearchResult
from delbot_platform.research.research_engine import ResearchEngine, research_analysis
from delbot_platform.workspace.session_manager import SessionManager

router = APIRouter()
_session_mgr = SessionManager()

class ResearchAskRequest(BaseModel):
    query: str
    history: list[dict] = []

class TitleGenRequest(BaseModel):
    interests: list[str] = []
    keywords: list[str] = []
    category: str = "general"
    preferred_method: str = ""

@router.post("/api/research/ask", response_model=ResearchResult, tags=["Research"])
def ask_research(
    session_id: str,
    request: ResearchAskRequest,
) -> ResearchResult:
    try:
        engine = ResearchEngine(session_manager=_session_mgr)
        return engine.ask(session_id=session_id, query=request.query, history=request.history)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/research/research-analysis", tags=["Research"])
def analyze_research(request: dict):
    query = request.get("query", "")
    session_id = request.get("session_id", "")
    active_docs = request.get("active_document_ids", [])
    return research_analysis(query=query, session_id=session_id, active_document_ids=active_docs)

@router.post("/thesis-title-generator", tags=["Research"])
async def generate_thesis_titles_endpoint(req: TitleGenRequest):
    from delbot_platform.research.generators.title_generator_service import generate_titles
    return await generate_titles(
        interests=req.interests,
        keywords=req.keywords,
        category=req.category,
        preferred_method=req.preferred_method
    )
