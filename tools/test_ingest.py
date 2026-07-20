import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.document.ingestion.qdrant_ingest import (
    QdrantIngest
)


db = QdrantIngest()


db.ensure_collection()


db.insert(
    """
DELBot adalah Digital Engineering Library Bot.

DELBot merupakan AI Research Operating System
untuk membantu penelitian akademik menggunakan
LLM, RAG, Document Intelligence,
Knowledge Retrieval dan Research Engine.
""",
    {
        "source": "manual",
        "type": "document",
        "title": "DELBot Overview"
    }
)


print(
    "INGEST SUCCESS"
)
