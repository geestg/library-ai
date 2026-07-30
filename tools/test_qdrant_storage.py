from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)
from delbot_platform.repository.integration.document_loader import (
    RepositoryDocumentLoader,
)
from delbot_platform.vectorstore import (
    QdrantRepository,
)


async def main() -> None:

    print("=" * 70)
    print("Loading Repository")
    print("=" * 70)

    loader = RepositoryDocumentLoader()

    documents = loader.load_available()

    if not documents:
        print("Repository kosong.")
        return

    target = documents[0]

    pdf_path = target["pdf_path"]

    print(f"PDF : {pdf_path}")
    print()

    pipeline = DocumentIndexingPipeline()

    started = time.perf_counter()

    artifact, summary = await pipeline.index_with_summary(
        pdf_path,
    )

    elapsed = time.perf_counter() - started

    repository = QdrantRepository()

    document_id = artifact.document.id

    print("=" * 70)
    print("Checking Qdrant")
    print("=" * 70)

    store = repository.store

    client = getattr(store, "client", None)
    collection = getattr(store, "collection_name", None)

    point_count = None

    if client is not None and collection is not None:

        scroll_result = client.scroll(
            collection_name=collection,
            scroll_filter={
                "must": [
                    {
                        "key": "document_id",
                        "match": {
                            "value": document_id,
                        },
                    },
                ],
            },
            with_payload=False,
            with_vectors=False,
            limit=100000,
        )

        points = scroll_result[0]
        point_count = len(points)

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"DOCUMENT ID : {document_id}")
    print(f"PAGES       : {summary.pages}")
    print(f"BLOCKS      : {summary.blocks}")
    print(f"SECTIONS    : {summary.sections}")
    print(f"CHUNKS      : {summary.chunks}")
    print(f"VECTORS     : {summary.vectors}")
    print(f"QDRANT      : {point_count}")
    print(f"TIME        : {elapsed:.2f}s")
    print()

    if point_count == summary.chunks:
        print("======================================")
        print("QDRANT STORAGE : PASS")
        print("======================================")
    else:
        print("======================================")
        print("QDRANT STORAGE : FAILED")
        print("Chunk Count :", summary.chunks)
        print("Point Count :", point_count)
        print("======================================")


if __name__ == "__main__":
    asyncio.run(main())
