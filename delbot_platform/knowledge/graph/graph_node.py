from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.knowledge_entity import (
    KnowledgeEntity,
)


@dataclass(slots=True)
class GraphNode:

    entity: KnowledgeEntity = field(
        default_factory=KnowledgeEntity,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def node_id(
        self,
    ) -> str:
        return self.entity.entity_id

    @property
    def entity_id(
        self,
    ) -> str:
        return self.entity.entity_id

    @property
    def name(
        self,
    ) -> str:
        return self.entity.name

    @property
    def entity_type(
        self,
    ) -> str:
        return self.entity.entity_type

    @property
    def aliases(
        self,
    ) -> list[str]:
        return self.entity.aliases

    @property
    def description(
        self,
    ) -> str:
        return self.entity.description

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "entity": self.entity.export(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "GraphNode":

        return cls(
            entity=KnowledgeEntity.from_dict(
                data.get(
                    "entity",
                    {},
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )
