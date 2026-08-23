from delbot_platform.research.embedding.query import QueryEmbedding
from delbot_platform.research.retrieval.qdrant_retriever import QdrantRetriever



class ResearchService:


    def __init__(self):

        self.embedding=QueryEmbedding()

        self.retriever=QdrantRetriever()



    def retrieve(
        self,
        question:str
    ):


        vector=self.embedding.embed(
            question
        )


        return self.retriever.search(
            vector
        )
