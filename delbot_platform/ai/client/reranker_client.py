from __future__ import annotations

import requests

from delbot_platform.core.config_manager import ConfigManager
from delbot_platform.knowledge.models import DocumentChunk


class RerankerClient:

    def __init__(
        self,
        url: str | None = None,
    ) -> None:

        if url is None:
            cfg = ConfigManager()
            service = cfg.service("reranker")
            host = service.get("host", "127.0.0.1")
            port = service["port"]
            url = f"http://{host}:{port}/v1/rerank"

        self.url = url

    def rerank(
        self,
        query: str,
        documents: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        texts = [
            document.text
            for document in documents
        ]

        response = requests.post(
            self.url,
            json={
                "query": query,
                "documents": texts,
            },
            timeout=600,
        )

        response.raise_for_status()

        ranked = response.json()["results"]

        output: list[DocumentChunk] = []

        for item in ranked:

            chunk = documents[item["index"]]

            chunk.rerank_score = float(
                item["score"]
            )

            output.append(chunk)

        return output
