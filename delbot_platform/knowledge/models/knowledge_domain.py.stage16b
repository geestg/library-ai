from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class KnowledgeDomain:

    domain_id: str = ""

    name: str = ""

    description: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "domain_id": self.domain_id,
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "KnowledgeDomain":

        return cls(
            domain_id=data.get(
                "domain_id",
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
            metadata=data.get(
                "metadata",
                {},
            ),
        )