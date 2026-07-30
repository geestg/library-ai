from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from delbot_platform.api.routers.document import (
    BatchIndexRequest,
    index_all,
)


async def main():

    response = await index_all(
        BatchIndexRequest(
            limit=20,
        )
    )

    print()
    print("==================================================")
    print("INDEX RESULT")
    print("==================================================")
    print("Success :", response.success)
    print("Indexed :", response.indexed)
    print("Skipped :", response.skipped)
    print("Total   :", response.total_pdf)
    print()

    assert response.success
    assert response.indexed == 20
    assert response.total_pdf >= 20

    print("PASS")


asyncio.run(main())
