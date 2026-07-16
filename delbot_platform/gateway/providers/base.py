from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.gateway.request import (
    ChatRequest,
    EmbeddingRequest,
)
from delbot_platform.gateway.openai.chat import (
    ChatCompletionResponse,
)
from delbot_platform.gateway.openai.embedding import (
    EmbeddingResponse,
)


class BaseProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatCompletionResponse:
        raise NotImplementedError

    @abstractmethod
    async def embedding(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        raise NotImplementedError