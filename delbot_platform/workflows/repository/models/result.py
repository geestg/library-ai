from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RepositoryIngestionResult:
    """
    Summary produced by the repository
    ingestion workflow.
    """

    repository_id: str

    document_id: str

    success: bool

    indexed: bool

    knowledge_created: bool

    elapsed: float
