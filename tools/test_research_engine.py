from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT),
)

from delbot_platform.research.research_engine import (
    ResearchEngine,
)
from delbot_platform.workspace.session_manager import (
    SessionManager,
)


async def main() -> None:

    sessions = SessionManager()

    session = sessions.create(
        title="Research Engine Test",
    )

    session_id = session["session_id"]

    engine = ResearchEngine(
        session_manager=sessions,
    )

    result = await engine.ask(
        session_id=session_id,
        query="Bagaimana metodologi penelitian machine learning?",
    )

    print("=" * 60)

    print("ANSWER")

    print("=" * 60)

    print(result.answer)

    print()

    print("=" * 60)

    print("CITATIONS")

    print("=" * 60)

    for citation in result.sources:

        print(citation)


if __name__ == "__main__":
    asyncio.run(main())