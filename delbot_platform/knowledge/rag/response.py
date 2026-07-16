from __future__ import annotations


from dataclasses import dataclass


from delbot_platform.knowledge.citation.source import (
    CitationSource,
)



@dataclass(slots=True)
class RAGResponse:


    context: str


    citations: list[CitationSource]