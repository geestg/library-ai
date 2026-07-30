from __future__ import annotations

import asyncio
import inspect
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from delbot_platform.application.research.answer import (
    ResearchAnswerApplication,
)

print("=" * 80)
print("DELBOT MVP")
print("CANONICAL APPLICATION VALIDATION")
print("=" * 80)


async def main():

    app = ResearchAnswerApplication()

    print()
    print("=" * 80)
    print("APPLICATION")
    print("=" * 80)

    print("TYPE :", type(app).__name__)
    print("ASYNC:", inspect.iscoroutinefunction(app.execute))

    print()
    print("=" * 80)
    print("RUN")
    print("=" * 80)

    response = await app.execute(
        question="PLC OMRON CPM2A dan Arduino Mega 2560"
    )

    print()
    print("=" * 80)
    print("RESPONSE")
    print("=" * 80)

    print(type(response).__name__)

    print()

    for name in dir(response):

        if name.startswith("_"):
            continue

        value = getattr(response, name)

        if callable(value):
            continue

        print(f"{name:20}", type(value).__name__)

    print()

    if hasattr(response, "answer"):
        print("=" * 80)
        print("ANSWER")
        print("=" * 80)
        print(response.answer[:1000])

    if hasattr(response, "rag"):

        rag = response.rag

        print()
        print("=" * 80)
        print("RAG")
        print("=" * 80)

        if hasattr(rag, "context"):
            print("Context :", len(rag.context))

        if hasattr(rag, "documents"):
            print("Documents :", len(rag.documents))

        if hasattr(rag, "citations"):
            print("Citations :", len(rag.citations))

    print()
    print("=" * 80)
    print("PASS")
    print("=" * 80)


try:

    asyncio.run(main())

except Exception:

    print()
    print("FAILED")
    print()

    traceback.print_exc()
