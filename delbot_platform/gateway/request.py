from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChatRequest:

    message: str

    model: str | None = None

    temperature: float = 0.7

    max_tokens: int | None = None


@dataclass(slots=True)
class EmbeddingRequest:

    text: str

    model: str | None = None


@dataclass(slots=True)
class VisionRequest:

    prompt: str

    image: str

    model: str | None = None