from __future__ import annotations

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)
from delbot_platform.gateway.mapper.embedding import (
    EmbeddingMapper,
)
from delbot_platform.gateway.providers.base import (
    BaseProvider,
)
from delbot_platform.gateway.request import (
    ChatRequest,
    EmbeddingRequest,
)
from delbot_platform.gateway.runtime.infinity import (
    InfinityRuntimeClient,
)


class InfinityProvider(BaseProvider):

    def __init__(
        self,
    ) -> None:

        self.registry = ModelRegistry()

    async def chat(
        self,
        request: ChatRequest,
    ):

        raise NotImplementedError(
            "Infinity backend does not support chat."
        )

    async def embedding(
        self,
        request: EmbeddingRequest,
    ):

        model = self.registry.default(
            ModelCategory.EMBEDDING,
        )

        runtime = InfinityRuntimeClient(
            model.runtime,
        )

        raw = runtime.embedding(
            {
                "input": request.text,
                "model": model.name,
            },
        )

        return EmbeddingMapper.from_runtime(
            raw,
        )