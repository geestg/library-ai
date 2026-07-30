from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT),
)

from delbot_platform.knowledge.retrieval.qdrant import (
    QdrantRetriever,
)


async def main() -> None:

    retriever = QdrantRetriever()

    results = await retriever.retrieve(
        query="Apa itu DELBot?",
        limit=5,
    )

    for item in results:

        print("=" * 60)

        print("ID:")
        print(item.id)

        print()

        print("SCORE:")
        print(item.score)

        print()

        print("CONTENT:")
        print(item.content[:300])

        print()

        print("SOURCE:")
        print(item.metadata.source)

        print()

        print("SECTION:")
        print(item.metadata.section)

        print()

        print("PAGE:")
        print(
            f"{item.metadata.page_start}"
            f"-{item.metadata.page_end}"
        )


if __name__ == "__main__":
    asyncio.run(main())