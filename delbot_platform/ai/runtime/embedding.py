from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


#
# Runtime Configuration
#

MODEL_NAME = os.getenv(
    "DELBOT_EMBEDDING_MODEL",
    "BAAI/bge-m3",
)

DEVICE = os.getenv(
    "DELBOT_EMBEDDING_DEVICE",
    "cpu",
)


#
# Load Model
#

model = SentenceTransformer(
    MODEL_NAME,
    device=DEVICE,
)


app = FastAPI(
    title="DELBot Embedding Runtime",
    version="1.0.0",
)


class EmbeddingRequest(BaseModel):

    model: str | None = None

    input: str


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "category": "embedding",
        "backend": "sentence-transformers",
        "model": MODEL_NAME,
        "device": DEVICE,
        "dimension": model.get_sentence_embedding_dimension(),
    }


@app.post("/v1/embeddings")
def embeddings(
    request: EmbeddingRequest,
):

    vector = model.encode(
        request.input,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return {
        "object": "list",
        "model": request.model or MODEL_NAME,
        "data": [
            {
                "object": "embedding",
                "index": 0,
                "embedding": vector.tolist(),
            }
        ],
    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8105,
    )
