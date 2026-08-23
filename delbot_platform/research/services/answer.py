from __future__ import annotations


from delbot_platform.knowledge.rag.research.pipeline import (
    ResearchAnswerPipeline,
)


from delbot_platform.knowledge.rag.llm.response import (
    LLMResponse,
)



class ResearchAnswerService:


    def __init__(
        self,
    ) -> None:


        self.pipeline = ResearchAnswerPipeline()



    async def answer(
        self,
        question: str,
    ) -> LLMResponse:


        return await self.pipeline.answer(

            question=question,

        )