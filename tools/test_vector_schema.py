from __future__ import annotations


import sys

from pathlib import Path


ROOT=Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.knowledge.rag.vector_retriever import VectorRetriever



retriever=VectorRetriever()


results=retriever.search(

    "bagaimana metodologi penelitian machine learning",

    3

)


for r in results:

    print("="*50)

    print(r.keys())

    print("TEXT:")

    print(r["text"][:300])

    print("SOURCE:")

    print(r["source"])

    print("PAGE:")

    print(r["page"])

    print("VECTOR SCORE:")

    print(r["vector_score"])
