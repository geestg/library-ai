from __future__ import annotations


from delbot_platform.vectorstore.qdrant.client import (
    QdrantVectorStore,
)



_store = None



def get_qdrant_store() -> QdrantVectorStore:


    global _store


    if _store is None:

        _store = QdrantVectorStore()


    return _store
