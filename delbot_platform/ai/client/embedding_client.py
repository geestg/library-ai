from __future__ import annotations

import requests

from delbot_platform.core.config_manager import ConfigManager


class EmbeddingClient:

    def __init__(
        self,
        url: str | None = None,
    ) -> None:

        if url is None:
            cfg = ConfigManager()
            service = cfg.service("embedding")
            host = service.get("host", "127.0.0.1")
            port = service["port"]
            url = f"http://{host}:{port}/v1/embeddings"

        self.url = url

    def embed(
        self,
        text: str,
    ):

        response = requests.post(
            self.url,
            json={
                "input": text,
            },
            timeout=600,
        )

        response.raise_for_status()

        data = response.json()

        if "data" in data:
            return data["data"][0]["embedding"]

        if "embedding" in data:
            return data["embedding"]

        raise RuntimeError(
            f"Invalid embedding response: {data}"
        )
