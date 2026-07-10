from dataclasses import dataclass
from dataclasses import field

from app.services.research.models.research_profile import (
    ResearchProfile,
)


# =====================================
# RESEARCH CONTEXT
# =====================================

@dataclass
class ResearchContext:

    # =================================
    # REQUEST
    # =================================

    query: str

    session_id: str = ""

    top_k: int = 10

    mode: str = "analysis"

    active_document_ids: list = field(
        default_factory=list
    )

    # =================================
    # CONVERSATION
    # =================================

    conversation_history: str = ""

    # =================================
    # QUERY
    # =================================

    normalized_query: str = ""

    query_domain: dict = field(
        default_factory=dict
    )

    # =================================
    # RETRIEVAL
    # =================================

    theses: list = field(
        default_factory=list
    )

    citations: list = field(
        default_factory=list
    )

    document_chunks: list = field(
        default_factory=list
    )

    # =================================
    # DOMAIN
    # =================================

    final_domain: dict = field(
        default_factory=dict
    )

    domain_instruction: str = ""

    # =================================
    # EVIDENCE
    # =================================

    evidence: dict = field(
        default_factory=dict
    )

    evidence_matrix: dict = field(
        default_factory=dict
    )

    combined_evidence: str = ""

    citation_context: str = ""

    # =================================
    # RESEARCH PROFILE
    # =================================

    research_profile: ResearchProfile = field(
        default_factory=ResearchProfile
    )

    # =================================
    # PROMPT
    # =================================

    prompt: str = ""

    # =================================
    # OUTPUT
    # =================================

    analysis: str = ""

    response: dict | None = None

    llm_stream: object = None

    # =================================
    # LLM
    # =================================

    provider: str = ""

    model: str = ""

    intent: str = ""

    # =================================
    # PIPELINE
    # =================================

    stage_results: dict = field(
        default_factory=dict
    )