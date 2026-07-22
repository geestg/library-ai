from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class WorkspaceMetadata:

    active_collection: str = ""

    active_document: str = ""

    selected_model: str = ""

    settings: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "active_collection": self.active_collection,
            "active_document": self.active_document,
            "selected_model": self.selected_model,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "WorkspaceMetadata":

        return cls(
            active_collection=data.get(
                "active_collection",
                "",
            ),
            active_document=data.get(
                "active_document",
                "",
            ),
            selected_model=data.get(
                "selected_model",
                "",
            ),
            settings=data.get(
                "settings",
                {},
            ),
        )