from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.author import Author
from delbot_platform.knowledge.models.collection import Collection
from delbot_platform.knowledge.models.knowledge_entity import KnowledgeEntity
from delbot_platform.knowledge.models.knowledge_relation import KnowledgeRelation


@dataclass(slots=True)
class Document:

    document_id: str = ""

    title: str = ""

    file_path: str = ""

    collection: Collection = field(
        default_factory=Collection,
    )

    authors: list[Author] = field(
        default_factory=list,
    )

    entities: list[KnowledgeEntity] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def collection_id(
        self,
    ) -> str:

        return self.collection.collection_id

    @property
    def collection_name(
        self,
    ) -> str:

        return self.collection.name

    @property
    def repository(
        self,
    ):

        return self.collection.repository

    @property
    def repository_id(
        self,
    ) -> str:

        return self.repository.repository_id

    @property
    def repository_name(
        self,
    ) -> str:

        return self.repository.name

    @property
    def repository_root_path(
        self,
    ) -> str:

        return self.repository.root_path

    @property
    def source(
        self,
    ):

        return self.repository.source

    @property
    def source_id(
        self,
    ) -> str:

        return self.source.source_id

    @property
    def source_name(
        self,
    ) -> str:

        return self.source.name

    @property
    def domain(
        self,
    ):

        return self.source.domain

    @property
    def domain_id(
        self,
    ) -> str:

        return self.domain.domain_id

    @property
    def domain_name(
        self,
    ) -> str:

        return self.domain.name

    @property
    def author_ids(
        self,
    ) -> list[str]:

        values: list[str] = []
        seen: set[str] = set()

        for author in self.authors:

            if not author.author_id:
                continue

            if author.author_id in seen:
                continue

            seen.add(
                author.author_id,
            )

            values.append(
                author.author_id,
            )

        return values

    @property
    def author_names(
        self,
    ) -> list[str]:

        values: list[str] = []
        seen: set[str] = set()

        for author in self.authors:

            if not author.full_name:
                continue

            if author.full_name in seen:
                continue

            seen.add(
                author.full_name,
            )

            values.append(
                author.full_name,
            )

        return values

    @property
    def relations(
        self,
    ) -> list[KnowledgeRelation]:

        relations: list[KnowledgeRelation] = []

        for entity in self.entities:
            relations.extend(
                entity.relations,
            )

        return relations

    @property
    def relation_ids(
        self,
    ) -> list[str]:

        values: list[str] = []
        seen: set[str] = set()

        for relation in self.relations:

            if not relation.relation_id:
                continue

            if relation.relation_id in seen:
                continue

            seen.add(
                relation.relation_id,
            )

            values.append(
                relation.relation_id,
            )

        return values

    @property
    def relation_types(
        self,
    ) -> list[str]:

        values: list[str] = []
        seen: set[str] = set()

        for relation in self.relations:

            if not relation.relation_type:
                continue

            if relation.relation_type in seen:
                continue

            seen.add(
                relation.relation_type,
            )

            values.append(
                relation.relation_type,
            )

        return values

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "document_id": self.document_id,
            "title": self.title,
            "file_path": self.file_path,
            "collection": self.collection.export(),
            "collection_id": self.collection_id,
            "collection_name": self.collection_name,
            "repository_id": self.repository_id,
            "repository_name": self.repository_name,
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
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Document":

        if "collection" in data:

            collection = Collection.from_dict(
                data["collection"],
            )

        else:

            from delbot_platform.knowledge.models import KnowledgeDomain
            from delbot_platform.knowledge.models import KnowledgeSource
            from delbot_platform.knowledge.models import Repository

            collection = Collection(
                collection_id=data.get(
                    "collection_id",
                    "",
                ),
                name=data.get(
                    "collection_name",
                    "",
                ),
                repository=Repository(
                    repository_id=data.get(
                        "repository_id",
                        "",
                    ),
                    name=data.get(
                        "repository_name",
                        "",
                    ),
                    source=KnowledgeSource(
                        source_id=data.get(
                            "source_id",
                            "",
                        ),
                        name=data.get(
                            "source_name",
                            "",
                        ),
                        domain=KnowledgeDomain(
                            domain_id=data.get(
                                "domain_id",
                                "",
                            ),
                            name=data.get(
                                "domain_name",
                                "",
                            ),
                        ),
                    ),
                ),
            )

        authors = [
            Author.from_dict(
                item,
            )
            for item in data.get(
                "authors",
                [],
            )
        ]

        entities = [
            KnowledgeEntity.from_dict(
                item,
            )
            for item in data.get(
                "entities",
                [],
            )
        ]

        return cls(
            document_id=data.get(
                "document_id",
                "",
            ),
            title=data.get(
                "title",
                "",
            ),
            file_path=data.get(
                "file_path",
                "",
            ),
            collection=collection,
            authors=authors,
            entities=entities,
            metadata=data.get(
                "metadata",
                {},
            ),
        )