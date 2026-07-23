from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class EmbeddingRequest:
    """
    Request sent to an embedding provider.

    One request represents one text that should be converted
    into a vector.
    """

    id: str

    text: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
