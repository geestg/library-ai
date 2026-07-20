from __future__ import annotations


from qdrant_client import QdrantClient


from delbot_platform.research.embedding.query import (
    QueryEmbedding,
)



class QdrantRetriever:


    COLLECTION = "delbot_documents"



    def __init__(self):

        self.client = QdrantClient(
            host="127.0.0.1",
            port=6333,
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
