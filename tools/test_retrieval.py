import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)



from delbot_platform.research.retrieval.qdrant_retriever import (
    QdrantRetriever
)



retriever = QdrantRetriever()



results = retriever.search(
    "Apa itu DELBot?"
)



for item in results:

    print(
        "===================="
    )

    print(
        "SCORE:",
        item["score"]
    )


    print(
        item["payload"]
    )
