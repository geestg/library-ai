from __future__ import annotations

import requests

from delbot_platform.knowledge.models import DocumentChunk


class RerankerClient:

    def __init__(
        self,
        url: str = "http://localhost:8106/v1/rerank",
    ) -> None:

        self.url = url

    def rerank(
        self,
        query: str,
        documents: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        texts = []

        for document in documents:

            texts.append(
                document.text
            )

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

            chunk = documents[
                item["index"]
            ]

            chunk.rerank_score = float(
                item["score"]
            )

            output.append(
                chunk
            )

        return output