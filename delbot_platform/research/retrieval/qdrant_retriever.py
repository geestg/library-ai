from __future__ import annotations


from qdrant_client import QdrantClient


from delbot_platform.research.embedding.query import (
    QueryEmbedding,
)



class QdrantRetriever:


    COLLECTION = "delbot_documents"



    def __init__(self):
        import os
        from delbot_platform.core.config import settings
        host = os.environ.get("QDRANT_HOST", settings.QDRANT_HOST)
        port = int(os.environ.get("QDRANT_PORT", settings.QDRANT_PORT))
        is_in_docker = os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER") == "1"
        if not is_in_docker and "host.docker.internal" in host:
            host = "127.0.0.1"

        self.client = QdrantClient(
            host=host,
            port=port,
        )


        self.embedding = QueryEmbedding()



    def search(
        self,
        query:str,
        limit:int = 5,
    ):


        vector = self.embedding.embed(
            query
        )


        results = self.client.search(
            collection_name=self.COLLECTION,
            query_vector=vector,
            limit=limit,
        )


        documents=[]


        for item in results:

            documents.append(
                {
                    "score": item.score,
                    "payload": item.payload,
                }
            )


        return documents
