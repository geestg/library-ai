from __future__ import annotations

import requests


class EmbeddingClient:


    def __init__(
        self,
        url="http://localhost:8105/v1/embeddings"
    ):

        self.url = url



    def embed(
        self,
        text: str
    ):

        response = requests.post(
            self.url,
            json={
                "input": text
            },
            timeout=600
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
