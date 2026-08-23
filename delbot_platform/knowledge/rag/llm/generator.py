from __future__ import annotations


from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)


from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)


from delbot_platform.gateway.client import (
    GatewayClient,
)


from delbot_platform.knowledge.citation.source import (
    CitationSource,
)


from delbot_platform.knowledge.rag.llm.response import (
    LLMResponse,
)



class LLMGenerator:


    def __init__(
        self,
    ) -> None:


        self.registry = ModelRegistry()

        self.client = GatewayClient()



    async def generate(
        self,
        context: str,
        citations: list[CitationSource],
        instruction: str | None = None,
    ) -> LLMResponse:


        runtime = self.registry.default(
            ModelCategory.CHAT,
        ).runtime



        payload = {

            "messages": [

                {

                    "role": "system",

                    "content":
                    (
                        "You are DELBot, "
                        "an academic research assistant. "
                        "Answer based on provided context."
                    ),

                },

                {

                    "role": "user",

                    "content":
                    (
                        f"Context:\n\n"
                        f"{context}\n\n"
                        f"Question:\n"
                        f"{instruction or ''}"
                    ),

                },

            ],

        }



        response = self.client.post(

            runtime=runtime,

            endpoint="/chat",

            payload=payload,

        )



        answer = response.get(
            "answer",
            "",
        )



        return LLMResponse(

            answer=answer,

            citations=citations,

        )