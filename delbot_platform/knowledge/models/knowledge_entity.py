from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from .knowledge_relation import KnowledgeRelation


@dataclass(slots=True)
class KnowledgeEntity:

    entity_id: str = ""

    name: str = ""

    entity_type: str = ""

    aliases: list[str] = field(
        default_factory=list,
    )

    description: str = ""

    relations: list["KnowledgeRelation"] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "entity_type": self.entity_type,
            "aliases": list(self.aliases),
            "description": self.description,
            "relations": [
                relation.export()
                for relation in self.relations
            ],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "KnowledgeEntity":

        from .knowledge_relation import KnowledgeRelation

        return cls(
            entity_id=data.get(
                "entity_id",
                "",
            ),
            name=data.get(
                "name",
                "",
            ),
            entity_type=data.get(
                "entity_type",
                "",
            ),
            aliases=list(
                data.get(
                    "aliases",
                    [],
                ),
            ),
            description=data.get(
                "description",
                "",
            ),
            relations=[
                KnowledgeRelation.from_dict(item)
                for item in data.get(
                    "relations",
                    [],
                )
            ],
            metadata=data.get(
                "metadata",
                {},
            ),
        )