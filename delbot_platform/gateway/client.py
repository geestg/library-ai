from __future__ import annotations

import httpx

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.gateway.router import (
    GatewayRouter,
)


class GatewayClient:

    def __init__(
        self,
        timeout: float = 30.0,
    ) -> None:

        self.timeout = timeout

        self.router = GatewayRouter()

    def _base_url(
        self,
        category: ModelCategory,
    ) -> str:

        runtime = self.router.runtime(
            category,
        )

        return (
            f"http://{runtime.host}:{runtime.port}"
        )

    def get(
        self,
        category: ModelCategory,
        endpoint: str,
    ):

        url = (
            self._base_url(category)
            + endpoint
        )

        response = httpx.get(
            url,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def post(
        self,
        category: ModelCategory,
        endpoint: str,
        payload: dict,
    ):

        url = (
            self._base_url(category)
            + endpoint
        )

        response = httpx.post(
            url,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()