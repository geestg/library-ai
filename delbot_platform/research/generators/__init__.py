from __future__ import annotations

from delbot_platform.research.generators.thesis_idea_generator import generate_thesis_ideas
from delbot_platform.research.generators.literature_review_generator import generate_literature_review
from delbot_platform.research.generators.analysis_engine import run_analysis
from delbot_platform.research.generators.thesis_prompts import build_thesis_ideas_prompt
from delbot_platform.research.generators.title_generator_service import generate_thesis_titles

__all__ = [
    "generate_thesis_ideas",
    "generate_literature_review",
    "run_analysis",
    "build_thesis_ideas_prompt",
    "generate_thesis_titles",
]
