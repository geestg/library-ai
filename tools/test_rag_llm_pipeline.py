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
    print("ASYNC RAG + LLM VALIDATION")
    print("=" * 80)
    print()

    try:
        from delbot_platform.research.pipeline.research_answer_pipeline import (
            ResearchAnswerPipeline,
        )

        print("IMPORT : PASS")
        print()

    except Exception:

        print("IMPORT : FAILED")
        print()
        traceback.print_exc()
        return

    print("=" * 80)
    print("PIPELINE")
    print("=" * 80)

    try:

        pipeline = ResearchAnswerPipeline()

        print("CREATE : PASS")

    except Exception:

        print("CREATE : FAILED")
        traceback.print_exc()
        return

    print()
    print("=" * 80)
    print("COMPONENTS")
    print("=" * 80)

    print("answer() async :", asyncio.iscoroutinefunction(pipeline.answer))
    print("RAG            :", type(pipeline.rag).__name__)
    print("PROMPT         :", type(pipeline.prompt_builder).__name__)
    print("LLM            :", type(pipeline.generator).__name__)

    print()
    print("=" * 80)
    print("RUN PIPELINE")
    print("=" * 80)

    try:

        answer, rag = await pipeline.answer(
            question="PLC OMRON CPM2A dan Arduino Mega 2560",
            history=[],
            previous="",
            research_state={},
        )

        print("PIPELINE : PASS")
        print()

        print("Context Length :", len(rag.context))
        print("Documents      :", len(rag.documents))
        print("Citations      :", len(rag.citations))
        print()

        print("=" * 80)
        print("ANSWER TYPE")
        print("=" * 80)

        print(type(answer))

        if hasattr(answer, "answer"):
            print()
            print(answer.answer[:1000])

        else:
            print()
            print(str(answer)[:1000])

    except Exception:

        print("PIPELINE : FAILED")
        print()
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

