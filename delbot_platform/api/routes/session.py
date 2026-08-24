from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from delbot_platform.research.models import ResearchResult
from delbot_platform.research.research_engine import ResearchEngine
from delbot_platform.workspace.session_manager import SessionManager
from delbot_platform.research.session import session_manager as academic_session_mgr

router = APIRouter()
workspace_session_manager = SessionManager()
research_engine = ResearchEngine(workspace_session_manager)


class CreateSessionRequest(BaseModel):
    title: str = "Untitled Research"


class AskRequest(BaseModel):
    query: str


# =========================================
# Workspace Sessions (Platform Layer)
# =========================================

@router.post("/api/workspace/session", tags=["Workspace"])
def create_workspace_session(body: CreateSessionRequest):
    return workspace_session_manager.create(body.title)


@router.get("/api/workspace/sessions", tags=["Workspace"])
def get_workspace_sessions():
    return [
        session.export()
        for session in workspace_session_manager.sessions.values()
    ]


@router.get("/api/workspace/{session_id}", tags=["Workspace"])
def get_workspace_session(session_id: str):
    session = workspace_session_manager.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.export()


@router.post("/api/workspace/{session_id}/ask", response_model=ResearchResult, tags=["Workspace"])
def ask_workspace(session_id: str, body: AskRequest):
    try:
        return research_engine.ask(session_id=session_id, query=body.query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Academic Research Sessions
# =========================================

@router.post("/session/create", tags=["Session"])
def create_academic_session(body: Optional[CreateSessionRequest] = None):
    session = academic_session_mgr.create()
    return {"session_id": session.session_id}


@router.get("/session/history", tags=["Session"])
def get_session_history(session_id: Optional[str] = None):
    if session_id:
        session = academic_session_mgr.get(session_id)
        if not session or not session.conversation:
            return {"session_id": session_id, "history": []}
        return {
            "session_id": session_id,
            "history": session.conversation.export(),
        }
    
    history_list = []
    for sid, s in academic_session_mgr._sessions.items():
        msgs = s.conversation.export() if s.conversation else []
        title = msgs[0].get("content", "Research Session")[:40] if msgs else "Research Workspace"
        history_list.append({
            "session_id": sid,
            "title": title,
            "message_count": len(msgs),
            "messages": msgs
        })
    return history_list


@router.get("/session/{session_id}", tags=["Session"])
def get_academic_session(session_id: str):
    session = academic_session_mgr.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    msgs = session.conversation.export() if session.conversation else []
    return {
        "session_id": session.session_id,
        "history": msgs,
        "conversation": {
            "messages": msgs
        },
        "active_documents": list(session.documents.documents.keys()) if session.documents else [],
    }


@router.get("/session/{session_id}/documents", tags=["Session"])
def get_session_documents(session_id: str):
    session = academic_session_mgr.get_session(session_id)
    if not session:
        return []
    return list(session.active_documents)
