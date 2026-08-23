from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.models.knowledge_entity import (
    KnowledgeEntity,
)
from delbot_platform.knowledge.models.knowledge_relation import (
    KnowledgeRelation,
)


@dataclass(slots=True)
class ExtractionResult:

    entities: list[KnowledgeEntity] = field(
        default_factory=list,
    )

    relations: list[KnowledgeRelation] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict:

        return {
            "entities": [
                entity.export()
                for entity in self.entities
            ],
            "relations": [
                relation.export()
                for relation in self.relations
            ],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ExtractionResult":

        return cls(
            entities=[
                KnowledgeEntity.from_dict(item)
                for item in data.get(
                    "entities",
                    [],
                )
            ],
            relations=[
                KnowledgeRelation.from_dict(item)
                for item in data.get(
                    "relations",
                    [],
                )
            ],
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )
