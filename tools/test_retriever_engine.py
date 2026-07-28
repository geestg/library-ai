from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT),
)

from delbot_platform.knowledge.retrieval.qdrant import (
    QdrantRetriever,
)


async def main():

    retriever = QdrantRetriever()

    query = """
    cara membuat penelitian machine learning
    """

    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(query.strip())

    results = await retriever.retrieve(
        query=query,
        limit=5,
    )

    print()
    print("=" * 80)
    print(f"HASIL : {len(results)}")
    print("=" * 80)

    for i, item in enumerate(results, start=1):

        print()
        print(f"RANK {i}")
        print("-" * 80)
        print("SCORE      :", item.score)
        print("DOCUMENT   :", item.metadata.document_id)
        print("SOURCE     :", item.metadata.source)
        print("SECTION    :", item.metadata.section)
        print("PAGE       :", f"{item.metadata.page_start}-{item.metadata.page_end}")
        print()
        print(item.content[:500])
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())
