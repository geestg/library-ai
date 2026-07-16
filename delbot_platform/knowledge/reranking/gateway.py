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


from delbot_platform.knowledge.reranking.base import (
    Reranker,
)

from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)



class GatewayReranker(
    Reranker,
):


    def __init__(
        self,
    ) -> None:


        self.registry = ModelRegistry()

        self.client = GatewayClient()



    async def rerank(
        self,
        query: str,
        documents: list[RerankResult],
        limit: int = 5,
    ) -> list[RerankResult]:


        runtime = self.registry.default(
            ModelCategory.RERANKER,
        ).runtime



        payload = {

            "query": query,

            "documents": [

                {

                    "id": item.id,

                    "text": item.content,

                }

                for item in documents

            ],

        }



        response = self.client.post(

            runtime=runtime,

            endpoint="/rerank",

            payload=payload,

        )



        ranked = []



        for item in response["results"][:limit]:


            original = next(

                document

                for document in documents

                if document.id == item["id"]

            )


            ranked.append(

                RerankResult(

                    id=original.id,

                    score=item["score"],

                    content=original.content,

                    metadata=original.metadata,

                )

            )



        return ranked