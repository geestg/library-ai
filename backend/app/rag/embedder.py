from app.services.embedder.embedding_gateway import (
    embedding_gateway
)


def get_embedding(text: str):

    return embedding_gateway.embed(text)