from __future__ import annotations

import sys

from pathlib import Path


ROOT=Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.knowledge.rag.rag_engine import RAGEngine



engine=RAGEngine()


result=engine.query(
    "bagaimana membuat metodologi penelitian machine learning"
)


print("="*60)

print(result["query"])


print("="*60)


print(
    result["context"][:5000]
)
