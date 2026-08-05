from __future__ import annotations

from enum import Enum


class ModelCategory(str, Enum):

    CHAT = "chat"

    FAST_CHAT = "fast_chat"

    CODING = "coding"

    VISION = "vision"

    EMBEDDING = "embedding"

    RERANKER = "reranker"

    OCR = "ocr"

    SPEECH = "speech"

    def __str__(self) -> str:

        return self.value