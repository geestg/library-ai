from __future__ import annotations

from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):

    model: str = "qwen3-32b"

    messages: List[ChatMessage] | None = None

    # legacy
    message: str | None = None

    temperature: float = 0.7

    max_tokens: int | None = None


    def get_message(self):

        if self.message:
            return self.message

        if self.messages:
            return self.messages[-1].content

        return ""



class EmbeddingRequest(BaseModel):

    model: str = "bge-m3"

    input: str

    
    @property
    def text(self):

        return self.input



class VisionRequest(BaseModel):

    model: str | None = None

    prompt: str

    image: str
