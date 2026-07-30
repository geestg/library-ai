from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path
from dataclasses import fields

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)

from delbot_platform.repository import (
    RepositoryDocumentLoader,
)


async def main():

    loader = RepositoryDocumentLoader()

    documents = loader.load_available()

    total = min(10, len(documents))

    print("=" * 60)
    print("TOTAL PDF :", total)
    print("=" * 60)
    print()

    pipeline = DocumentIndexingPipeline()

    success = 0
    failed = 0

    started_all = time.perf_counter()

    for index, document in enumerate(documents[:total], start=1):

        pdf_path = document["pdf_path"]

        print("-" * 60)
        print(f"[{index}/{total}]")
        print(Path(pdf_path).name)

        started = time.perf_counter()

        try:

            artifact, summary = await pipeline.index_with_summary(
                pdf_path,
            )

            elapsed = time.perf_counter() - started

            success += 1

            print("STATUS     : PASS")
            print(f"PAGES      : {summary.pages}")
            print(f"BLOCKS     : {summary.blocks}")
            print(f"SECTIONS   : {summary.sections}")
            print(f"CHUNKS     : {summary.chunks}")
            print(f"VECTORS    : {summary.vectors}")
            print(f"TIME       : {elapsed:.2f}s")

        except Exception as exc:

            failed += 1

            elapsed = time.perf_counter() - started

            print("STATUS     : FAILED")
            print(type(exc).__name__)
            print(exc)
            print(f"TIME       : {elapsed:.2f}s")

        print()

    total_elapsed = time.perf_counter() - started_all

    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print("SUCCESS :", success)
    print("FAILED  :", failed)
    print("TOTAL   :", total)
    print(f"ELAPSED : {total_elapsed:.2f}s")

    print()

    if failed == 0:
        print("BATCH PIPELINE PASS")
    else:
        print("BATCH PIPELINE HAS FAILURE")


asyncio.run(main())
