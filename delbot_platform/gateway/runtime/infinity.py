from __future__ import annotations

from typing import Any

from delbot_platform.ai.registry.model_runtime import (
    ModelRuntime,
)
from delbot_platform.gateway.client import (
    GatewayClient,
)


class InfinityRuntimeClient:

    def __init__(
        self,
        runtime: ModelRuntime,
        client: GatewayClient | None = None,
    ) -> None:

        self.runtime = runtime

        self.client = client or GatewayClient()

    def health(
        self,
    ) -> Any:

        return self.client.get(
            runtime=self.runtime,
            endpoint="/health",
        )

    def embedding(
        self,
        payload: dict,
    ) -> Any:

        return self.client.post(
            runtime=self.runtime,
            endpoint="/embeddings",
            payload=payload,
        )