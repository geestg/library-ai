from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class KnowledgeRelation:

    relation_id: str = ""

    source_entity_id: str = ""

    target_entity_id: str = ""

    relation_type: str = ""

    weight: float = 1.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "relation_id": self.relation_id,
            "source_entity_id": self.source_entity_id,
            "target_entity_id": self.target_entity_id,
            "relation_type": self.relation_type,
            "weight": self.weight,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "KnowledgeRelation":

        return cls(
            relation_id=data.get(
                "relation_id",
                "",
            ),
            source_entity_id=data.get(
                "source_entity_id",
                "",
            ),
            target_entity_id=data.get(
                "target_entity_id",
                "",
            ),
            relation_type=data.get(
                "relation_type",
                "",
            ),
            weight=float(
                data.get(
                    "weight",
                    1.0,
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )