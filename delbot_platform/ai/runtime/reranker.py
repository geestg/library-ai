from __future__ import annotations


from fastapi import FastAPI
from pydantic import BaseModel

from sentence_transformers import CrossEncoder


app = FastAPI(
    title="DELBot Reranker Service"
)



MODEL = CrossEncoder(
    "BAAI/bge-reranker-v2-m3"
)



class RerankRequest(BaseModel):

    query: str

    documents: list[str]



@app.get("/health")
def health():

    return {
        "status":"healthy",
        "category":"reranker",
        "model":"bge-reranker-v2-m3"
    }



@app.post("/v1/rerank")
def rerank(
    request:RerankRequest
):


    pairs=[]


    for doc in request.documents:

        pairs.append(
            [
                request.query,
                doc
            ]
        )



    scores = MODEL.predict(
        pairs
    )


    results=[]


    for index,score in enumerate(scores):


        results.append(
            {
                "index":index,
                "score":float(score),
                "text":request.documents[index]
            }
        )



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return {

        "results":results

    }

import uvicorn


if __name__ == "__main__":

    uvicorn.run(
        "delbot_platform.ai.runtime.reranker:app",
        host="0.0.0.0",
        port=8106,
        reload=False,
    )
