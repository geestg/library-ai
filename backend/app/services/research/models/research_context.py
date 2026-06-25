from dataclasses import dataclass
from dataclasses import field


# =====================================
# RESEARCH CONTEXT
# =====================================

@dataclass
class ResearchContext:

    # =================================
    # INPUT
    # =================================

    query: str

    top_k: int = 10

    mode: str = "analysis"

    active_document_ids: list = field(
        default_factory=list
    )

    # =================================
    # SEARCH
    # =================================

    normalized_query: str = ""

    query_domain: dict = field(
        default_factory=dict
    )

    theses: list = field(
        default_factory=list
    )

    citations: list = field(
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

    gap_analysis: dict = field(
        default_factory=dict
    )

    novelty_analysis: dict = field(
        default_factory=dict
    )

    trend_analysis: dict = field(
        default_factory=dict
    )

    competency_analysis: dict = field(
        default_factory=dict
    )

    prodi_analysis: dict = field(
        default_factory=dict
    )

    competency_analysis: dict = field(
        default_factory=dict
    )
    
    # =================================
    # CONTEXT
    # =================================

    combined_evidence: str = ""

    citation_context: str = ""

    # =================================
    # OUTPUT
    # =================================

    prompt: str = ""

    analysis: str = ""