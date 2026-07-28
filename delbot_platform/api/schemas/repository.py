from __future__ import annotations

from pydantic import BaseModel


class RepositoryIndexRequest(BaseModel):

    id: str

    title: str

    repository_url: str

    pdf_url: str | None = None


class RepositoryIndexResponse(BaseModel):

    repository_id: str

    document_id: str

    success: bool

    indexed: bool

    knowledge_created: bool

    elapsed: float
