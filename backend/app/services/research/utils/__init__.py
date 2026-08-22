from __future__ import annotations

from app.services.research.utils.domain_classifier import detect_domain
from app.services.research.utils.domain_resolver import resolve_domain
from app.services.research.utils.evidence_extractor import extract_evidence
from app.services.research.utils.evidence_matrix import build_evidence_matrix
from app.services.research.utils.novelty_scorer import calculate_novelty_score
from app.services.research.utils.trend_engine import build_research_trends

__all__ = [
    "detect_domain",
    "resolve_domain",
    "extract_evidence",
    "build_evidence_matrix",
    "calculate_novelty_score",
    "build_research_trends",
]
