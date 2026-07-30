from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI(
    title="DELBot Embedding Runtime"
)


class EmbeddingRequest(BaseModel):

    model: str | None = None

    input: str



@app.get("/health")
def health():

    return {
        "status": "healthy",
        "category": "embedding",
        "model": "bge-m3",
        "backend": "infinity"
    }



@app.post("/embeddings")
def embeddings(
    request: EmbeddingRequest
):

    # temporary runtime validation
    # nanti diganti inference asli infinity

    vector = [
        0.01,
        0.02,
        0.03
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

        "model": request.model or "bge-m3"

    }



if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8105
    )
