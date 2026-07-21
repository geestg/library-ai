from __future__ import annotations



from delbot_platform.knowledge.rag.rag_engine import RAGEngine
from delbot_platform.ai.client.llm_client import LLMClient
from delbot_platform.research.prompt_builder import ResearchPromptBuilder




class ResearchEngine:



    def __init__(self):


        self.rag = RAGEngine()

        self.llm = LLMClient()

        self.prompt = ResearchPromptBuilder()




    def ask(

        self,

        query:str

    ):



        retrieval=self.rag.search(

            query

        )



        messages=self.prompt.build(

            query,

            retrieval["context"]

        )



        answer=self.llm.chat(

            messages

        )



        return {


            "answer":answer,


            "citations":

            retrieval["citations"],


            "sources":

            retrieval["documents"]

        }
