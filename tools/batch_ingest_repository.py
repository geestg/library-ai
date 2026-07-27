from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT),
)

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)
from delbot_platform.repository import (
    RepositoryDocumentLoader,
)
from delbot_platform.vectorstore import (
    QdrantRepository,
)


async def main() -> None:

    print("=" * 60)
    print("DELBot Repository Batch Indexer")
    print("=" * 60)

    loader = RepositoryDocumentLoader()

    pipeline = DocumentIndexingPipeline()

    repository = QdrantRepository()

    documents = loader.load_available()

    print(f"PDF COUNT : {len(documents)}")

    indexed = 0
    failed = 0

    for index, document in enumerate(
        documents,
        start=1,
    ):

        pdf_path = document["pdf_path"]

        print()
        print(
            f"[{index}/{len(documents)}]",
            Path(pdf_path).name,
        )

        try:

            artifact = await pipeline.index(
                pdf_path,
            )

            print(
                f"Sections : {len(artifact.sections)}"
            )

            print(
                f"Chunks   : {len(artifact.chunks)}"
            )

            print(
                f"Vectors  : {len(artifact.vectors)}"
            )

            indexed += 1

        except Exception as exc:

            failed += 1

            print(
                "FAILED:",
                exc,
            )

    print()
    print("=" * 60)

    print(
        "Indexed Documents :",
        indexed,
    )

    print(
        "Failed Documents  :",
        failed,
    )

    print(
        "Total Vectors     :",
        repository.count(),
    )


if __name__ == "__main__":
    asyncio.run(
        main(),
    )