from __future__ import annotations


from qdrant_client import QdrantClient

from delbot_platform.ai.client.embedding_client import EmbeddingClient



class VectorRetriever:


    def __init__(
        self,
        collection="delbot_documents"
    ):

        self.collection = collection


        self.qdrant = QdrantClient(
            host="localhost",
            port=6333
        )


        self.embedder = EmbeddingClient()



    def search(
        self,
        query:str,
        limit:int=10
    ):


        vector = self.embedder.embed(
            [query]
        )[0]


        results = self.qdrant.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=limit,
            with_payload=True
        )


        output=[]


        for r in results:

            output.append(
                {
                    "score":r.score,

                    "payload":r.payload
                }
            )


        return output
