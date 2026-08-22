from typing import List, Optional
from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default_session"
    top_k: int = 10
    mode: str = "analysis"
    active_document_ids: Optional[List[str]] = []
