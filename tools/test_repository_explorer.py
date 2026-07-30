from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from delbot_platform.api.routers.repository import (
    repository_explorer,
)

async def main():

    result = await repository_explorer()

    print()
    print("==================================================")
    print("REPOSITORY EXPLORER")
    print("==================================================")
    print("Total         :", result.total)
    print("PDF Available :", result.pdf_available)
    print("PDF Missing   :", result.pdf_missing)
    print("Items         :", len(result.items))
    print()

    assert result.total == len(result.items)

    print("PASS")

    print()

    print("FIRST 10 ITEMS")

    for item in result.items[:10]:

        print(
            item.id,
            "|",
            item.status,
            "|",
            item.title[:80],
        )

asyncio.run(main())
