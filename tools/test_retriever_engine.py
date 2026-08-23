from __future__ import annotations


import sys

from pathlib import Path


ROOT=Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.knowledge.retrieval.retriever import VectorRetriever



retriever=VectorRetriever()



query="""
cara membuat penelitian machine learning
"""


print("="*60)
print(query)
print("="*60)



results=retriever.search(
    query,
    limit=5
)



for i,r in enumerate(results):

    print()
    print("RANK",i+1)

    print(
        "SCORE:",
        r["score"]
    )


    payload=r["payload"]


    print(
        payload.get(
            "source_file",
            ""
        )
    )


    print(
        payload.get(
            "text",
            ""
        )[:500]
    )


    print("-"*60)
