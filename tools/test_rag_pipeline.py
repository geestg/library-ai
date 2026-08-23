from __future__ import annotations


import sys

from pathlib import Path



ROOT = Path(__file__).resolve().parent.parent


sys.path.insert(
    0,
    str(ROOT)
)



from delbot_platform.knowledge.rag.rag_engine import RAGEngine




query = "bagaimana metodologi penelitian machine learning"



print("="*60)

print(query)

print("="*60)



engine = RAGEngine()



result = engine.search(
    query,
    limit=5
)



print()

print("DOCUMENTS")

print("="*60)



for index,doc in enumerate(
    result["documents"],
    start=1
):


    print()

    print(
        "RANK",
        index
    )


    print(
        "VECTOR SCORE:",
        doc.get(
            "vector_score"
        )
    )


    print(
        "RERANK SCORE:",
        doc.get(
            "rerank_score"
        )
    )


    print(
        "SOURCE:",
        doc.get(
            "source"
        )
    )


    print(
        "PAGE:",
        doc.get(
            "page"
        )
    )


    print(
        "TEXT:"
    )


    print(
        doc["text"][:500]
    )


    print(
        "-"*60
    )



print()

print("CITATIONS")

print("="*60)



for c in result["citations"]:

    print(c)



print()

print("CONTEXT LENGTH")

print(
    len(
        result["context"]
    )
)
