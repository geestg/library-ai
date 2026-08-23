from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmbeddingConfig:
    """
    Configuration for embedding providers.
    """

    base_url: str

    model: str

    timeout: float = 300.0

    api_key: str | None = None

    batch_size: int = 64
