"""
Qdrant vector-store package.

The authoritative implementation is QdrantStore in singleton.py.
QdrantVectorStore is retained only as a compatibility alias for existing
package consumers during the MVP transition.
"""

from .singleton import QdrantStore, get_qdrant_store

QdrantVectorStore = QdrantStore

__all__ = [
    "QdrantStore",
    "QdrantVectorStore",
    "get_qdrant_store",
]
from .repository import QdrantRepository
