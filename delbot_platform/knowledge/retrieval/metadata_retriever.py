from __future__ import annotations


from delbot_platform.knowledge.retrieval.retriever import VectorRetriever



class MetadataRetriever:


    def __init__(self):

        self.retriever = VectorRetriever(
            "delbot_metadata"
        )



    def search(
        self,
        query:str,
        limit:int=5
    ):


        return self.retriever.search(
            query,
            limit
        )
