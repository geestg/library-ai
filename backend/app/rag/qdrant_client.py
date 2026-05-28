from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams
)

from app.core.config import settings


client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    timeout=120,
)


def ensure_collection_exists(
    collection_name: str,
    vector_size: int = 768,
):

    collections = client.get_collections()

    exists = any(
        c.name == collection_name
        for c in collections.collections
    )

    if not exists:

        client.create_collection(

            collection_name=collection_name,

            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(
            f"[QDRANT] Collection created: "
            f"{collection_name}"
        )

    else:

        print(
            f"[QDRANT] Collection already exists: "
            f"{collection_name}"
        )