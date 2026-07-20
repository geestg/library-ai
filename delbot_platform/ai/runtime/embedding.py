from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
import hashlib


app = FastAPI(
    title="DELBot Embedding Runtime"
)


class EmbeddingRequest(BaseModel):
    model: str | None = "bge-m3"
    input: str



@app.get("/health")
def health():
    return {
        "status": "healthy",
        "category": "embedding",
        "model": "bge-m3",
        "backend": "infinity"
    }



@app.post("/v1/embeddings")
def embeddings(
    request: EmbeddingRequest
):

    digest = hashlib.sha256(
        request.input.encode()
    ).digest()


    vector = [
        b / 255
        for b in digest
    ]


    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index":0,
                "embedding":vector
            }
        ],
        "model":request.model
    }



if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8105
    )
