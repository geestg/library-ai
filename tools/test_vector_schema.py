from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT),
)

from delbot_platform.knowledge.rag.vector_retriever import (
    VectorRetriever,
)


retriever = VectorRetriever()

results = retriever.search(
    "bagaimana metodologi penelitian machine learning",
    3,
)

for chunk in results:

    print("=" * 60)

    exported = chunk.export()

    print(exported.keys())

    print()

    print("TEXT:")
    print(chunk.text[:300])

    print()

    print("SOURCE:")
    print(chunk.source_name)

    print()

    print("PAGE:")
    print(chunk.page)

    print()

    print("VECTOR SCORE:")
    print(chunk.vector_score)