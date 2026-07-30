from __future__ import annotations

import asyncio
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


async def main():

    print("=" * 80)
    print("DELBOT MVP")
    print("PRODUCTION END-TO-END TEST")
    print("=" * 80)

    try:
        from delbot_platform.application.research.answer import (
            ResearchAnswerApplication,
        )

        print()
        print("IMPORT : PASS")

    except Exception:
        print()
        print("IMPORT : FAILED")
        traceback.print_exc()
        return

    app = ResearchAnswerApplication()

    print()
    print("=" * 80)
    print("APPLICATION")
    print("=" * 80)

    print(type(app).__name__)

    print()
    print("=" * 80)
    print("EXECUTE")
    print("=" * 80)

    response = await app.execute(
        question="PLC OMRON CPM2A dan Arduino Mega 2560"
    )

    print("TYPE :", type(response).__name__)

    print()
    print("=" * 80)
    print("RESPONSE VALIDATION")
    print("=" * 80)

    checks = [
        ("answer", hasattr(response, "answer")),
        ("citations", hasattr(response, "citations")),
        ("rag", hasattr(response, "rag")),
    ]

    failed = False

    for name, ok in checks:
        print(f"{name:15}", ok)
        if not ok:
            failed = True

    if failed:
        print()
        print("FAILED")
        return

    rag = response.rag

    print()
    print("=" * 80)
    print("RAG")
    print("=" * 80)

    print("Context Length :", len(rag.context))
    print("Documents      :", len(rag.documents))
    print("Citations      :", len(rag.citations))

    print()
    print("=" * 80)
    print("ANSWER PREVIEW")
    print("=" * 80)

    print(response.answer[:1000])

    print()
    print("=" * 80)
    print("ASSERTIONS")
    print("=" * 80)

    assert len(response.answer.strip()) > 0
    assert len(rag.context) > 0
    assert len(rag.documents) > 0
    assert len(rag.citations) > 0
    assert len(response.citations) > 0

    print("PASS : Answer")
    print("PASS : Context")
    print("PASS : Documents")
    print("PASS : Citations")
    print("PASS : Pipeline")

    print()
    print("=" * 80)
    print("MVP PRODUCTION PIPELINE VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

