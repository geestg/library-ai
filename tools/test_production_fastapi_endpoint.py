from __future__ import annotations

import asyncio
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 80)
print("DELBOT MVP")
print("PRODUCTION FASTAPI ENDPOINT VALIDATION")
print("=" * 80)

try:
    from delbot_platform.gateway.routers.research import (
        ResearchRequest,
        ResearchResponse,
        research_answer,
    )

    print()
    print("=" * 80)
    print("IMPORT")
    print("=" * 80)
    print("PASS")

except Exception:
    print()
    print("IMPORT FAILED")
    traceback.print_exc()
    raise SystemExit(1)


async def main():

    print()
    print("=" * 80)
    print("REQUEST")
    print("=" * 80)

    request = ResearchRequest(
        question="PLC OMRON CPM2A dan Arduino Mega 2560",
    )

    print(request)

    print()
    print("=" * 80)
    print("CALL ENDPOINT")
    print("=" * 80)

    response = await research_answer(request)

    print()
    print("=" * 80)
    print("TYPE")
    print("=" * 80)

    print(type(response).__name__)

    print()
    print("=" * 80)
    print("FIELDS")
    print("=" * 80)

    print("answer          :", isinstance(response.answer, str))
    print("citations       :", isinstance(response.citations, list))
    print("context_length  :", response.context_length)
    print("documents       :", response.documents)
    print("retrieved       :", response.retrieved)

    print()
    print("=" * 80)
    print("ANSWER PREVIEW")
    print("=" * 80)

    print(response.answer[:1200])

    print()
    print("=" * 80)
    print("ASSERTIONS")
    print("=" * 80)

    assert isinstance(response, ResearchResponse)
    assert len(response.answer) > 0
    assert response.context_length > 0
    assert response.documents > 0
    assert response.retrieved > 0

    print("PASS : Response")
    print("PASS : Answer")
    print("PASS : Context")
    print("PASS : Documents")
    print("PASS : Retrieved")

    print()
    print("=" * 80)
    print("FASTAPI ENDPOINT VERIFIED")
    print("=" * 80)


asyncio.run(main())
