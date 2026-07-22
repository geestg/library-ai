from __future__ import annotations


from delbot_platform.knowledge.rag.vector_retriever import VectorRetriever
from delbot_platform.ai.client.reranker_client import RerankerClient
from delbot_platform.knowledge.rag.context_builder import ContextBuilder
from delbot_platform.knowledge.rag.citation_builder import CitationBuilder



class RAGEngine:


    def __init__(self):

        self.retriever = VectorRetriever()

        self.reranker = RerankerClient()

        self.builder = ContextBuilder()

        self.citation = CitationBuilder()



    def search(
        self,
        query:str,
        limit:int=5
    ):


        documents = self.retriever.search(
            query,
            limit=20
        )


        ranked = self.reranker.rerank(
            query,
            documents
        )


        ranked = ranked[:limit]



        return {


            "query":query,


            "documents":ranked,


            "context":self.builder.build(
                ranked
            ),


            "citations":self.citation.build(
                ranked
            )


        }
