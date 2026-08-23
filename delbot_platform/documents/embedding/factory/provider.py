from __future__ import annotations


from delbot_platform.documents.embedding.base import (
    EmbeddingService,
)


from delbot_platform.documents.embedding.providers.local import (
    LocalEmbeddingProvider,
)


from delbot_platform.documents.embedding.providers.gateway import (
    GatewayEmbeddingProvider,
)



class EmbeddingProviderFactory:


    @staticmethod
    def build(
        provider: str = "local",
    ) -> EmbeddingService:


        if provider == "local":

            return LocalEmbeddingProvider()


        if provider == "gateway":

            return GatewayEmbeddingProvider()


        raise ValueError(
            f"Unknown embedding provider: {provider}"
        )