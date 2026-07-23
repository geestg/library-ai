from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.knowledge.models.knowledge_relation import (
    KnowledgeRelation,
)


@dataclass(slots=True)
class GraphEdge:

    relation: KnowledgeRelation = field(
        default_factory=KnowledgeRelation,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def edge_id(
        self,
    ) -> str:
        return self.relation.relation_id

    @property
    def relation_id(
        self,
    ) -> str:
        return self.relation.relation_id

    @property
    def source_node_id(
        self,
    ) -> str:
        return self.relation.source_entity_id

    @property
    def target_node_id(
        self,
    ) -> str:
        return self.relation.target_entity_id

    @property
    def relation_type(
        self,
    ) -> str:
        return self.relation.relation_type

    @property
    def weight(
        self,
    ) -> float:
        return self.relation.weight

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "relation": self.relation.export(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "GraphEdge":

        return cls(
            relation=KnowledgeRelation.from_dict(
                data.get(
                    "relation",
                    {},
                ),
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )
