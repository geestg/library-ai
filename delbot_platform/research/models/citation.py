from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from delbot_platform.knowledge.models import (
    Author,
    Collection,
    Document,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeRelation,
    KnowledgeSource,
    Repository,
)


@dataclass(slots=True)
class Citation:
    document: Document

    page: int = 0
    chunk_id: str = ""
    score: float = 0.0
    text: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def document_id(self) -> str:
        return self.document.document_id

    @property
    def document_title(self) -> str:
        return self.document.title

    @property
    def file_path(self) -> str:
        return self.document.file_path

    @property
    def collection(self) -> Collection:
        return self.document.collection

    @property
    def collection_id(self) -> str:
        return self.document.collection.collection_id

    @property
    def collection_name(self) -> str:
        return self.document.collection.name

    @property
    def repository(self) -> Repository:
        return self.document.repository

    @property
    def repository_id(self) -> str:
        return self.document.repository.repository_id

    @property
    def repository_name(self) -> str:
        return self.document.repository.name

    @property
    def repository_root_path(self) -> str:
        return self.document.repository.root_path

    @property
    def source(self) -> KnowledgeSource:
        return self.document.source

    @property
    def source_id(self) -> str:
        return self.document.source.source_id

    @property
    def source_name(self) -> str:
        return self.document.source.name

    @property
    def domain(self) -> KnowledgeDomain:
        return self.document.domain

    @property
    def domain_id(self) -> str:
        return self.document.domain.domain_id

    @property
    def domain_name(self) -> str:
        return self.document.domain.name

    @property
    def authors(self) -> list[Author]:
        return self.document.authors

    @property
    def author_ids(self) -> list[str]:
        return self.document.author_ids

    @property
    def author_names(self) -> list[str]:
        return self.document.author_names

    @property
    def entities(self) -> list[KnowledgeEntity]:
        return self.document.entities

    @property
    def relation_ids(self) -> list[str]:
        return self.document.relation_ids

    @property
    def relation_types(self) -> list[str]:
        return self.document.relation_types

    @property
    def relations(self) -> list[KnowledgeRelation]:
        return self.document.relations

    def export(self) -> dict[str, Any]:
        return {
            "document": self.document.export(),
            "document_id": self.document.document_id,
            "document_title": self.document.title,
            "file_path": self.document.file_path,
            "collection_id": self.collection_id,
            "collection_name": self.collection_name,
            "repository_id": self.repository_id,
            "repository_name": self.repository_name,
            "repository_root_path": self.repository_root_path,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "authors": [
                author.export()
                for author in self.authors
            ],
            "author_ids": self.author_ids,
            "author_names": self.author_names,
            "entities": [
                entity.export()
                for entity in self.entities
            ],
            "relation_ids": self.relation_ids,
            "relation_types": self.relation_types,
            "page": self.page,
            "chunk_id": self.chunk_id,
            "score": self.score,
            "text": self.text,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Citation":
        if "document" in data:
            document = Document.from_dict(data["document"])
        else:
            document = Document.from_dict(data)

        return cls(
            document=document,
            page=data.get("page", 0),
            chunk_id=data.get("chunk_id", ""),
            score=data.get("score", 0.0),
            text=data.get("text", ""),
            metadata=data.get("metadata", {}),
        )