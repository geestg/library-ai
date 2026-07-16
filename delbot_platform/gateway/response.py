from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChatResponse:

    content: str

    model: str


@dataclass(slots=True)
class EmbeddingResponse:

    embedding: list[float]

    model: str


@dataclass(slots=True)
class VisionResponse:

    content: str

    model: str