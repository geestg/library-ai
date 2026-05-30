from app.rag.reranker import (
    rerank
)


def rerank_theses(
    query,
    theses
):

    documents = []

    for thesis in theses:

        text = f"""
        {thesis.get('title', '')}

        {thesis.get('abstract', '')}

        {thesis.get('chunk', '')}
        """

        documents.append({

            "text": text,

            "payload": thesis
        })

    ranked = rerank(

        query=query,

        documents=documents
    )

    results = []

    for item in ranked:

        results.append(
            item["payload"]
        )

    return results