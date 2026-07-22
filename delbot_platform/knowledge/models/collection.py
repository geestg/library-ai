from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.repository import Repository


@dataclass(slots=True)
class Collection:

    collection_id: str = ""

    name: str = ""

    description: str = ""

    repository: Repository = field(
        default_factory=Repository,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

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
    def source_id(
        self,
    ) -> str:

        return self.repository.source.source_id

    @property
    def source_name(
        self,
    ) -> str:

        return self.repository.source.name

    @property
    def domain_id(
        self,
    ) -> str:

        return self.repository.source.domain.domain_id

    @property
    def domain_name(
        self,
    ) -> str:

        return self.repository.source.domain.name

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "collection_id": self.collection_id,
            "name": self.name,
            "description": self.description,
            "repository": self.repository.export(),
            "repository_id": self.repository.repository_id,
            "repository_name": self.repository.name,
            "source_id": self.repository.source.source_id,
            "source_name": self.repository.source.name,
            "domain_id": self.repository.source.domain.domain_id,
            "domain_name": self.repository.source.domain.name,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Collection":

        if "repository" in data:

            repository = Repository.from_dict(
                data["repository"],
            )

        else:

            from delbot_platform.knowledge.models import KnowledgeDomain
            from delbot_platform.knowledge.models import KnowledgeSource

            repository = Repository(
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
            )

        return cls(
            collection_id=data.get(
                "collection_id",
                "",
            ),
            name=data.get(
                "name",
                "",
            ),
            description=data.get(
                "description",
                "",
            ),
            repository=repository,
            metadata=data.get(
                "metadata",
                {},
            ),
        )