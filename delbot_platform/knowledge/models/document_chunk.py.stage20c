from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.author import Author
from delbot_platform.knowledge.models.document import Document
from delbot_platform.knowledge.models.knowledge_entity import (
    KnowledgeEntity,
)


@dataclass(slots=True)
class DocumentChunk:

    chunk_id: str = ""

    document: Document = field(
        default_factory=Document,
    )

    page: int = 0

    text: str = ""

    vector_score: float = 0.0

    rerank_score: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def document_id(
        self,
    ) -> str:
        return self.document.document_id

    @property
    def document_title(
        self,
    ) -> str:
        return self.document.title

    @property
    def file_path(
        self,
    ) -> str:
        return self.document.file_path

    @property
    def collection_id(
        self,
    ) -> str:
        return self.document.collection.collection_id

    @property
    def collection_name(
        self,
    ) -> str:
        return self.document.collection.name

    @property
    def repository_id(
        self,
    ) -> str:
        return self.document.collection.repository.repository_id

    @property
    def repository_name(
        self,
    ) -> str:
        return self.document.collection.repository.name

    @property
    def repository_root_path(
        self,
    ) -> str:
        return self.document.collection.repository.root_path

    @property
    def source_id(
        self,
    ) -> str:
        return self.document.source_id

    @property
    def source_name(
        self,
    ) -> str:
        return self.document.source_name

    @property
    def domain_id(
        self,
    ) -> str:
        return self.document.domain_id

    @property
    def domain_name(
        self,
    ) -> str:
        return self.document.domain_name

    @property
    def domain(
        self,
    ):
        return self.document.domain

    @property
    def authors(
        self,
    ) -> list[Author]:
        return self.document.authors

    @property
    def author_ids(
        self,
    ) -> list[str]:
        return self.document.author_ids

    @property
    def author_names(
        self,
    ) -> list[str]:
        return self.document.author_names

    @property
    def entities(
        self,
    ) -> list[KnowledgeEntity]:
        return self.document.entities

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "chunk_id": self.chunk_id,
            "document": self.document.export(),
            "document_id": self.document.document_id,
            "document_title": self.document.title,
            "file_path": self.document.file_path,
            "collection_id": self.document.collection.collection_id,
            "collection_name": self.document.collection.name,
            "repository_id": self.document.collection.repository.repository_id,
            "repository_name": self.document.collection.repository.name,
            "repository_root_path": self.document.collection.repository.root_path,
            "source_id": self.document.source_id,
            "source_name": self.document.source_name,
            "domain_id": self.document.domain_id,
            "domain_name": self.document.domain_name,
            "authors": [
                author.export()
                for author in self.document.authors
            ],
            "author_ids": self.document.author_ids,
            "author_names": self.document.author_names,
            "entities": [
                entity.export()
                for entity in self.document.entities
            ],
            "page": self.page,
            "text": self.text,
            "vector_score": self.vector_score,
            "rerank_score": self.rerank_score,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DocumentChunk":

        if "document" in data:
            document = Document.from_dict(
                data["document"],
            )
        else:
            document = Document.from_dict(
                data,
            )

        return cls(
            chunk_id=data.get(
                "chunk_id",
                "",
            ),
            document=document,
            page=data.get(
                "page",
                0,
            ),
            text=data.get(
                "text",
                "",
            ),
            vector_score=data.get(
                "vector_score",
                0.0,
            ),
            rerank_score=data.get(
                "rerank_score",
                0.0,
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )