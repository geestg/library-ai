from __future__ import annotations

from typing import Any

import httpx


class HttpClient:
    """
    Lightweight HTTP client shared by all AI providers.
    """

    def __init__(
        self,
        *,
        base_url: str,
        timeout: float = 300.0,
        headers: dict[str, str] | None = None,
    ) -> None:

        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=headers,
        )

    @property
    def base_url(
        self,
    ) -> str:
        return self._base_url

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:

        response = self._client.get(
            path,
            **kwargs,
        )

        response.raise_for_status()

        return response

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:

        response = self._client.post(
            path,
            json=json,
            **kwargs,
        )

        response.raise_for_status()

        return response

    def close(
        self,
    ) -> None:

        self._client.close()

    def __enter__(
        self,
    ) -> "HttpClient":

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        self.close()
