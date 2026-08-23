from __future__ import annotations


from dataclasses import dataclass, field


from delbot_platform.knowledge.citation.source import (
    CitationSource,
)



@dataclass(slots=True)
class LLMResponse:


    answer: str


    citations: list[CitationSource] = field(
        default_factory=list,
    )