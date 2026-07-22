from __future__ import annotations

from qdrant_client import QdrantClient

from delbot_platform.ai.client.embedding_client import EmbeddingClient
from delbot_platform.knowledge.models import DocumentChunk


class VectorRetriever:

    def __init__(
        self,
        collection: str = "delbot_documents",
    ) -> None:

        self.collection = collection

        self.client = QdrantClient(
            host="localhost",
            port=6333,
        )

        self.embedding = EmbeddingClient()

    def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[DocumentChunk]:

        vector = self.embedding.embed(
            query,
        )

        results = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=limit,
            with_payload=True,
        )

        documents: list[DocumentChunk] = []

        for item in results:

            payload = item.payload or {}

            text = (
                payload.get("text")
                or payload.get("content")
                or payload.get("chunk_text")
                or ""
            )

            chunk = DocumentChunk(
                chunk_id=str(item.id),
                document_id=payload.get(
                    "document_id",
                    "",
                ),
                document_title=payload.get(
                    "document_title",
                    "",
                ),
                file_path=payload.get(
                    "source_file",
                    payload.get(
                        "file",
                        "",
                    ),
                ),
                page=payload.get(
                    "page",
                    0,
                ),
                text=text,
                vector_score=float(
                    item.score,
                ),
                metadata=payload,
            )

            documents.append(
                chunk,
            )

        return documents