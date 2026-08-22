from __future__ import annotations

from app.services.research.gap.gap_detector import detect_research_gaps
from app.services.research.gap.bab5_extractor import extract_bab5_gaps

__all__ = [
    "detect_research_gaps",
    "extract_bab5_gaps",
]
