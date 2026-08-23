import sys
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]


sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.research.services.rag import (
    RAGService
)



rag = RAGService()



result = rag.answer(
    "Apa itu DELBot?"
)



print(
    result["context"]
)
