from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from delbot_platform.gateway.routers.research import (
    ResearchRequest,
    research_answer,
)

async def main():

    response = await research_answer(
        ResearchRequest(
            question="PLC OMRON CPM2A dan Arduino Mega 2560",
        )
    )

    print("=" * 80)
    print("RESPONSE")
    print("=" * 80)

    print(type(response).__name__)

    print()

    print("Context Length :", response.context_length)
    print("Documents      :", response.documents)
    print("Retrieved      :", response.retrieved)

    print()

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(response.answer[:1000])

asyncio.run(main())
