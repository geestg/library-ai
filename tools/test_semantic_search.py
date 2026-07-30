from __future__ import annotations

import asyncio
import sys
import time
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qdrant_client.models import Filter

from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)
from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)

QUERY = "PLC OMRON CPM2A dan Arduino Mega 2560"


async def main() -> None:

    print("=" * 70)
    print("QUERY")
    print("=" * 70)
    print(QUERY)
    print()

    chunk = DocumentChunk(
        document_id="query",
        chunk_id=str(uuid.uuid4()),
        page_start=1,
        page_end=1,
        section_title="query",
        text=QUERY,
    )

    started = time.perf_counter()

    pipeline = EmbeddingPipeline()

    vectors = await pipeline.run(
        [chunk],
    )

    if not vectors:
        raise RuntimeError(
            "EmbeddingPipeline menghasilkan 0 vector."
        )

    query_vector = vectors[0].vector

    store = get_qdrant_store()

    print("=" * 70)
    print("SEARCH")
    print("=" * 70)

    results = store.search(
        query_vector=query_vector,
        limit=5,
        query_filter=Filter(),
        with_payload=True,
        with_vectors=False,
    )

    elapsed = time.perf_counter() - started

    print()

    print("=" * 70)
    print("RESULT")
    print("=" * 70)

    print(f"HITS : {len(results)}")
    print(f"TIME : {elapsed:.2f}s")
    print()

    if not results:
        print("SEMANTIC SEARCH : FAILED")
        return

    for i, hit in enumerate(results, start=1):

        payload = hit.payload or {}

        print("-" * 70)
        print(f"TOP {i}")
        print(f"SCORE        : {hit.score:.6f}")
        print(f"DOCUMENT     : {payload.get('document_id')}")
        print(f"SOURCE       : {payload.get('source')}")
        print(f"SECTION      : {payload.get('section_title')}")
        print(
            f"PAGES        : {payload.get('page_start')} - {payload.get('page_end')}"
        )

        text = payload.get("text", "")
        text = text.replace("\n", " ")

        if len(text) > 300:
            text = text[:300] + "..."

        print("TEXT")
        print(text)
        print()

    print("=" * 70)
    print("SEMANTIC SEARCH : PASS")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
