from __future__ import annotations

import httpx



class EmbeddingClient:


    def __init__(self):

        self.url="http://127.0.0.1:8100/v1/embeddings"



    def embed(
        self,
        text:str,
    ):


        response=httpx.post(
            self.url,
            json={
                "model":"bge-m3",
                "input":text,
            },
            timeout=60,
        )


        response.raise_for_status()


        data=response.json()


        return data["data"][0]["embedding"]
