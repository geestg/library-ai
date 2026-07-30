from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from delbot_platform.api.routers.repository import (
    RepositoryScanRequest,
    scan_repository,
)


async def main():

    req = RepositoryScanRequest(
        path="delbot_platform/repository_data/pdf",
    )

    res = await scan_repository(req)

    print()
    print("==================================================")
    print("SCAN RESULT")
    print("==================================================")
    print("Repository :", res.repository)
    print("Exists     :", res.exists)
    print("PDF Files  :", res.pdf_files)
    print("Metadata   :", res.metadata_files)
    print("Total      :", res.total_files)

    assert res.exists is True

    print()
    print("PASS")


asyncio.run(main())
