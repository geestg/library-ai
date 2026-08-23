from __future__ import annotations



class Reranker:


    def __init__(self):

        pass



    def rerank(
        self,
        query,
        documents,
        limit=5
    ):


        # temporary semantic fallback
        documents.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        return documents[:limit]
