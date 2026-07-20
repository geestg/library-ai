from __future__ import annotations



from delbot_platform.research.retrieval.qdrant_retriever import (
    QdrantRetriever,
)



from delbot_platform.research.rag.context import (
    ResearchContextBuilder,
)



from delbot_platform.research.llm.chat_client import (
    ChatClient,
)




class RAGService:



    def __init__(self):

        self.retriever = QdrantRetriever()

        self.context = ResearchContextBuilder()

        self.llm = ChatClient()




    def answer(
        self,
        question:str
    ):


        documents = self.retriever.search(
            question
        )


        context = self.context.build(
            documents
        )


        prompt = f"""
Anda adalah DELBot,
AI Research Operating System.

Gunakan context berikut untuk menjawab.

CONTEXT:

{context}


QUESTION:

{question}


Berikan jawaban akademik yang jelas.
"""


        answer = self.llm.chat(
            prompt
        )


        return {

            "question":question,

            "context":context,

            "answer":answer

        }
