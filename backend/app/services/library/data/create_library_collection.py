from __future__ import annotations

from qdrant_client.models import Distance, VectorParams
from app.core.constants import LIBRARY_BOOKS_COLLECTION
from app.rag.qdrant_client import client, ensure_collection_exists


def create_collection():
    """
    Membuat koleksi library_books di Qdrant dengan dimensi 768 untuk embedding nomic-embed-text.
    """
    ensure_collection_exists(
        collection_name=LIBRARY_BOOKS_COLLECTION,
        vector_size=768
    )
    print(f"[QDRANT] Collection {LIBRARY_BOOKS_COLLECTION} verified/created with 768 dimensions.")


if __name__ == "__main__":
    create_collection()
