from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any
from app.services.research.models.profile_models import ResearchProfile


@dataclass
class ResearchContext:
    query: str
    session_id: str = ""
    top_k: int = 10
    mode: str = "analysis"
    requested_prodi: str = ""
    active_document_ids: list = field(default_factory=list)
    conversation_history: str = ""
    normalized_query: str = ""
    query_domain: dict = field(default_factory=dict)
    theses: list = field(default_factory=list)
    citations: list = field(default_factory=list)
    final_domain: dict = field(default_factory=dict)
    domain_instruction: str = ""
    evidence: dict = field(default_factory=dict)
    evidence_matrix: dict = field(default_factory=dict)
    combined_evidence: str = ""
    citation_context: str = ""
    research_profile: ResearchProfile = field(default_factory=ResearchProfile)
    prompt: str = ""
    analysis: str = ""
    response: dict | None = None
    llm_stream: object = None
    provider: str = ""
    model: str = ""
    intent: str = ""
    stage_results: dict = field(default_factory=dict)
