from __future__ import annotations

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)
from delbot_platform.gateway.mapper.chat import (
    ChatCompletionMapper,
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
from delbot_platform.gateway.runtime.vllm import (
    VLLMRuntimeClient,
)


class VLLMProvider(BaseProvider):

    def __init__(
        self,
    ) -> None:

        self.registry = ModelRegistry()

    async def chat(
        self,
        request: ChatRequest,
    ):

        model = self.registry.default(
            ModelCategory.CHAT,
        )

        runtime = VLLMRuntimeClient(
            model.runtime,
        )

        raw = runtime.chat(
            {
                "model": model.name,
                "messages": [
                    {
                        "role": "user",
                        "content": request.get_message(),
                    }
                ],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            },
        )

        return ChatCompletionMapper.from_runtime(
            raw,
        )

    async def embedding(
        self,
        request: EmbeddingRequest,
    ):

        model = self.registry.default(
            ModelCategory.EMBEDDING,
        )

        runtime = VLLMRuntimeClient(
            model.runtime,
        )

        raw = runtime.embedding(
            {
                "model": model.name,
                "input": request.text,
            },
        )

        return EmbeddingMapper.from_runtime(
            raw,
        )