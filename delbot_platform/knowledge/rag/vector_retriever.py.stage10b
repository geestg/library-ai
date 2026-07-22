from __future__ import annotations


from qdrant_client import QdrantClient


from delbot_platform.ai.client.embedding_client import EmbeddingClient




class VectorRetriever:



    def __init__(

        self,

        collection="delbot_documents"

    ):


        self.collection = collection


        self.client = QdrantClient(

            host="localhost",

            port=6333

        )


        self.embedding = EmbeddingClient()




    def search(

        self,

        query:str,

        limit:int=10

    ):


        vector = self.embedding.embed(

            query

        )



        results = self.client.search(

            collection_name=self.collection,

            query_vector=vector,

            limit=limit,

            with_payload=True

        )



        documents=[]



        for item in results:


            payload=item.payload or {}



            text = (

                payload.get("text")

                or

                payload.get("content")

                or

                payload.get("chunk_text")

                or

                ""

            )



            documents.append(

                {


                    "id":str(item.id),


                    "text":text,


                    "vector_score":float(item.score),


                    "source":payload.get(

                        "source_file",

                        payload.get(

                            "file",

                            ""

                        )

                    ),


                    "page":payload.get(

                        "page",

                        0

                    ),


                    "payload":payload


                }

            )



        return documents
