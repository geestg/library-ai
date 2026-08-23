from __future__ import annotations


from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)

from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)

from delbot_platform.gateway.providers.factory import (
    ProviderFactory,
)

from delbot_platform.gateway.request import (
    ChatRequest,
    EmbeddingRequest,
)

from delbot_platform.gateway.response import (
    ChatResponse,
    EmbeddingResponse,
)



class GatewayService:


    def __init__(
        self,
    ) -> None:

        self.registry = ModelRegistry()



    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:


        model = self.registry.default(
            ModelCategory.CHAT,
        )


        provider = ProviderFactory.build(
            model.backend,
        )


        return await provider.chat(
            request,
        )



    async def embedding(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:


        model = self.registry.default(
            ModelCategory.EMBEDDING,
        )


        provider = ProviderFactory.build(
            model.backend,
        )


        return await provider.embedding(
            request,
        )
