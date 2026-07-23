from __future__ import annotations

from typing import Any
from typing import Callable
from typing import TypeVar

from delbot_platform.knowledge.models.author import Author
from delbot_platform.research.models.citation import Citation
from delbot_platform.research.models.research_result import (
    ResearchResult,
)

T = TypeVar("T")


class ResearchResultBuilder:

    def build(
        self,
        *,
        answer: str,
        citations: list[Citation],
        research_state: dict[str, Any],
    ) -> ResearchResult:

        authors = self._collect_authors(
            citations,
        )

        collections = self._collect_unique(
            citations,
            lambda c: c.collection_id,
            lambda c: c.collection_name,
        )

        repositories = self._collect_unique(
            citations,
            lambda c: c.repository_id,
            lambda c: c.repository_name,
        )

        knowledge_sources = self._collect_unique(
            citations,
            lambda c: c.source_id,
            lambda c: c.source_name,
        )

        knowledge_domains = self._collect_unique(
            citations,
            lambda c: c.domain_id,
            lambda c: c.domain_name,
        )

        entities = self._collect_entities(
            citations,
        )

        return ResearchResult(
            answer=answer,
            sources=citations,
            authors=authors,
            author_ids=[
                author.author_id
                for author in authors
            ],
            author_names=[
                author.full_name
                for author in authors
            ],
            collections=[
                item[1]
                for item in collections
            ],
            collection_ids=[
                item[0]
                for item in collections
            ],
            repositories=[
                item[1]
                for item in repositories
            ],
            repository_ids=[
                item[0]
                for item in repositories
            ],
            knowledge_sources=[
                item[1]
                for item in knowledge_sources
            ],
            knowledge_source_ids=[
                item[0]
                for item in knowledge_sources
            ],
            knowledge_domains=[
                item[1]
                for item in knowledge_domains
            ],
            knowledge_domain_ids=[
                item[0]
                for item in knowledge_domains
            ],
            entities=[
                item[1]
                for item in entities
            ],
            entity_ids=[
                item[0]
                for item in entities
            ],
            research_state=research_state,
        )

    def _collect_authors(
        self,
        citations: list[Citation],
    ) -> list[Author]:

        authors: list[Author] = []
        seen: set[str] = set()

        for citation in citations:

            for author in citation.authors:

                if author.author_id in seen:
                    continue

                seen.add(
                    author.author_id,
                )

                authors.append(
                    author,
                )

        return authors

    def _collect_unique(
        self,
        citations: list[Citation],
        id_getter: Callable[[Citation], str],
        value_getter: Callable[[Citation], str],
    ) -> list[tuple[str, str]]:

        results: list[tuple[str, str]] = []
        seen: set[str] = set()

        for citation in citations:

            item_id = id_getter(
                citation,
            )

            if item_id in seen:
                continue

            seen.add(
                item_id,
            )

            results.append(
                (
                    item_id,
                    value_getter(
                        citation,
                    ),
                ),
            )

        return results

    def _collect_entities(
        self,
        citations: list[Citation],
    ) -> list[tuple[str, str]]:

        entities: list[tuple[str, str]] = []
        seen: set[str] = set()

        for citation in citations:

            for entity in citation.entities:

                if entity.entity_id in seen:
                    continue

                seen.add(
                    entity.entity_id,
                )

                entities.append(
                    (
                        entity.entity_id,
                        entity.name,
                    ),
                )

        return entities