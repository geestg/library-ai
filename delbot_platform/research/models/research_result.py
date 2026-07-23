from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.author import Author
from delbot_platform.research.models.citation import Citation


@dataclass(slots=True)
class ResearchResult:

    answer: str

    sources: list[Citation] = field(
        default_factory=list,
    )

    authors: list[Author] = field(
        default_factory=list,
    )

    author_ids: list[str] = field(
        default_factory=list,
    )

    author_names: list[str] = field(
        default_factory=list,
    )

    collections: list[str] = field(
        default_factory=list,
    )

    collection_ids: list[str] = field(
        default_factory=list,
    )

    repositories: list[str] = field(
        default_factory=list,
    )

    repository_ids: list[str] = field(
        default_factory=list,
    )

    knowledge_sources: list[str] = field(
        default_factory=list,
    )

    knowledge_source_ids: list[str] = field(
        default_factory=list,
    )

    knowledge_domains: list[str] = field(
        default_factory=list,
    )

    knowledge_domain_ids: list[str] = field(
        default_factory=list,
    )

    entities: list[str] = field(
        default_factory=list,
    )

    entity_ids: list[str] = field(
        default_factory=list,
    )

    research_state: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "answer": self.answer,
            "sources": [
                source.export()
                for source in self.sources
            ],
            "authors": [
                author.export()
                for author in self.authors
            ],
            "author_ids": self.author_ids,
            "author_names": self.author_names,
            "collections": self.collections,
            "collection_ids": self.collection_ids,
            "repositories": self.repositories,
            "repository_ids": self.repository_ids,
            "knowledge_sources": self.knowledge_sources,
            "knowledge_source_ids": self.knowledge_source_ids,
            "knowledge_domains": self.knowledge_domains,
            "knowledge_domain_ids": self.knowledge_domain_ids,
            "entities": self.entities,
            "entity_ids": self.entity_ids,
            "research_state": self.research_state,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ResearchResult":

        return cls(
            answer=data.get(
                "answer",
                "",
            ),
            sources=[
                Citation.from_dict(item)
                for item in data.get(
                    "sources",
                    [],
                )
            ],
            authors=[
                Author.from_dict(item)
                for item in data.get(
                    "authors",
                    [],
                )
            ],
            author_ids=data.get(
                "author_ids",
                [],
            ),
            author_names=data.get(
                "author_names",
                [],
            ),
            collections=data.get(
                "collections",
                [],
            ),
            collection_ids=data.get(
                "collection_ids",
                [],
            ),
            repositories=data.get(
                "repositories",
                [],
            ),
            repository_ids=data.get(
                "repository_ids",
                [],
            ),
            knowledge_sources=data.get(
                "knowledge_sources",
                [],
            ),
            knowledge_source_ids=data.get(
                "knowledge_source_ids",
                [],
            ),
            knowledge_domains=data.get(
                "knowledge_domains",
                [],
            ),
            knowledge_domain_ids=data.get(
                "knowledge_domain_ids",
                [],
            ),
            entities=data.get(
                "entities",
                [],
            ),
            entity_ids=data.get(
                "entity_ids",
                [],
            ),
            research_state=data.get(
                "research_state",
                {},
            ),
        )