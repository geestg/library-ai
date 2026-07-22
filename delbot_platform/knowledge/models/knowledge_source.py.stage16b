from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.knowledge_domain import (
    KnowledgeDomain,
)


@dataclass(slots=True)
class KnowledgeSource:

    source_id: str = ""

    name: str = ""

    description: str = ""

    domain: KnowledgeDomain = field(
        default_factory=KnowledgeDomain,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

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

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "source_id": self.source_id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain.export(),
            "domain_id": self.domain.domain_id,
            "domain_name": self.domain.name,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "KnowledgeSource":

        if "domain" in data:

            domain = KnowledgeDomain.from_dict(
                data["domain"],
            )

        else:

            domain = KnowledgeDomain(
                domain_id=data.get(
                    "domain_id",
                    "",
                ),
                name=data.get(
                    "domain_name",
                    "",
                ),
            )

        return cls(
            source_id=data.get(
                "source_id",
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
            domain=domain,
            metadata=data.get(
                "metadata",
                {},
            ),
        )