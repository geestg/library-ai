from __future__ import annotations

from typing import Any

import httpx

from delbot_platform.ai.registry.model_runtime import (
    ModelRuntime,
)
from delbot_platform.gateway.exceptions import (
    GatewayTimeout,
    GatewayUnavailable,
)


class GatewayClient:

    def __init__(
        self,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:

        self.timeout = timeout

        self.retries = retries

    def _build_url(
        self,
        runtime: ModelRuntime,
        endpoint: str,
    ) -> str:

        return (
            f"http://{runtime.host}:{runtime.port}"
            f"{endpoint}"
        )

    def request(
        self,
        runtime: ModelRuntime,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:

        url = self._build_url(
            runtime,
            endpoint,
        )

        last_error: Exception | None = None

        for _ in range(
            self.retries,
        ):

            try:

                response = httpx.request(
                    method=method,
                    url=url,
                    json=payload,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                return response.json()

            except httpx.TimeoutException as exc:

                last_error = exc

            except httpx.HTTPError as exc:

                last_error = exc

        if isinstance(
            last_error,
            httpx.TimeoutException,
        ):

            raise GatewayTimeout(
                str(last_error),
            ) from last_error

        raise GatewayUnavailable(
            str(last_error),
        ) from last_error

    def get(
        self,
        runtime: ModelRuntime,
        endpoint: str,
    ):

        return self.request(
            runtime=runtime,
            method="GET",
            endpoint=endpoint,
        )

    def post(
        self,
        runtime: ModelRuntime,
        endpoint: str,
        payload: dict[str, Any],
    ):

        return self.request(
            runtime=runtime,
            method="POST",
            endpoint=endpoint,
            payload=payload,
        )