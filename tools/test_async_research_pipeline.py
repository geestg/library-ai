from __future__ import annotations

import asyncio
import inspect
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


async def main():

    print("=" * 80)
    print("FULL ASYNC RESEARCH PIPELINE")
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

    print()
    print("=" * 80)
    print("CREATE APPLICATION")
    print("=" * 80)

    app = ResearchAnswerApplication()

    print("PASS")

    print()
    print("=" * 80)
    print("TYPE CHECK")
    print("=" * 80)

    print(
        "Application.answer async :",
        inspect.iscoroutinefunction(app.answer),
    )

    print(
        "Service                 :",
        type(app.service).__name__,
    )

    print(
        "Pipeline                :",
        type(app.service.pipeline).__name__,
    )

    print(
        "RAG                     :",
        type(app.service.pipeline.rag).__name__,
    )

    print(
        "Prompt                  :",
        type(app.service.pipeline.prompt_builder).__name__,
    )

    print(
        "Generator               :",
        type(app.service.pipeline.generator).__name__,
    )

    print()
    print("=" * 80)
    print("RUN")
    print("=" * 80)

    try:

        answer, rag = await app.answer(
            question="PLC OMRON CPM2A dan Arduino Mega 2560"
        )

        print()
        print("PIPELINE : PASS")
        print()

        print("ANSWER TYPE :", type(answer).__name__)
        print("DOCS        :", len(rag.documents))
        print("CITATIONS   :", len(rag.citations))
        print("CONTEXT LEN :", len(rag.context))

        print()
        print("=" * 80)
        print("ANSWER PREVIEW")
        print("=" * 80)
        print()

        if isinstance(answer, str):
            print(answer[:1500])

        else:
            print(answer)

    except Exception:

        print()
        print("PIPELINE : FAILED")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

