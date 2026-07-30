from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from delbot_platform.repository.integration.document_loader import (
    RepositoryDocumentLoader,
)
from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)
from delbot_platform.vectorstore import (
    QdrantRepository,
)


async def main():

    print("=" * 70)
    print("LOAD PDF")
    print("=" * 70)

    loader = RepositoryDocumentLoader()

    document = loader.load_available()[0]

    print(document)

    print()
    print("=" * 70)
    print("RUN INDEX")
    print("=" * 70)

    pipeline = DocumentIndexingPipeline()

    artifact = await pipeline.index(
        document["pdf_path"],
    )

    print("Chunks :", artifact.chunk_count)
    print("Vectors:", artifact.vector_count)

    print()
    print("=" * 70)
    print("REPOSITORY")
    print("=" * 70)

    repo = QdrantRepository()

    print("Repository :", type(repo).__name__)
    print("Store      :", type(repo.store).__name__)
    print("Collection :", repo.store.collection)

    print()
    print("=" * 70)
    print("HEALTH")
    print("=" * 70)

    print(repo.store.health())

    print()
    print("=" * 70)
    print("TOTAL COUNT")
    print("=" * 70)

    try:
        total = repo.count()
        print(total)
    except Exception as exc:
        print(type(exc).__name__, exc)

    print()
    print("=" * 70)
    print("SCROLL DOCUMENT")
    print("=" * 70)

    try:

        points, _ = repo.store.scroll(
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document["document_id"],
                        ),
                    )
                ]
            ),
            with_payload=True,
            with_vectors=False,
            limit=1000,
        )

        print("FOUND :", len(points))

        if points:
            print("FIRST PAYLOAD")
            print(points[0].payload)

    except Exception as exc:
        print(type(exc).__name__, exc)

    print()
    print("=" * 70)
    print("COLLECTION INFO")
    print("=" * 70)

    try:
        print(repo.store.collection_info())
    except Exception as exc:
        print(type(exc).__name__, exc)


if __name__ == "__main__":
    asyncio.run(main())
