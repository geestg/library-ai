from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgePipelineResult:
    """
    Result produced by the canonical
    Knowledge Pipeline.
    """

    document_id: str

    extracted_entities: int = 0

    extracted_relations: int = 0

    graph_nodes: int = 0

    graph_edges: int = 0

    success: bool = True
