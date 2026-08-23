from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class Author:

    author_id: str = ""

    full_name: str = ""

    email: str = ""

    orcid: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def export(
        self,
    ) -> dict[str, Any]:

        return {
            "author_id": self.author_id,
            "full_name": self.full_name,
            "email": self.email,
            "orcid": self.orcid,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Author":

        return cls(
            author_id=data.get(
                "author_id",
                "",
            ),
            full_name=data.get(
                "full_name",
                "",
            ),
            email=data.get(
                "email",
                "",
            ),
            orcid=data.get(
                "orcid",
                "",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )