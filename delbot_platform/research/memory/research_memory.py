from __future__ import annotations

import json

from datetime import datetime
from pathlib import Path
from typing import Any


class ResearchMemory:

    def __init__(self) -> None:

        self.base = Path("runtime/research_memory")

        self.base.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _file(
        self,
        session_id: str,
    ) -> Path:

        return self.base / f"{session_id}.json"

    def _default_memory(self) -> dict[str, Any]:

        now = datetime.utcnow().isoformat()

        return {
            "history": [],
            "last_query": "",
            "last_answer": "",
            "summary": "",
            "topics": [],
            "keywords": [],
            "sources": [],
            "notes": [],
            "timeline": [],
            "research_state": {},
            "created_at": now,
            "updated_at": now,
        }

    def load(
        self,
        session_id: str,
    ) -> dict[str, Any]:

        file = self._file(
            session_id
        )

        if not file.exists():

            return self._default_memory()

        data = json.loads(
            file.read_text(
                encoding="utf-8",
            )
        )

        memory = self._default_memory()

        memory.update(data)

        return memory

    def save(
        self,
        session_id: str,
        query: str,
        answer: str,
        *,
        research_state: dict[str, Any] | None = None,
        summary: str | None = None,
        keywords: list[str] | None = None,
        sources: list[Any] | None = None,
        notes: list[Any] | None = None,
        timeline: list[Any] | None = None,
    ) -> dict[str, Any]:

        data = self.load(
            session_id
        )

        data["history"].append(
            {
                "role": "user",
                "content": query,
            }
        )

        data["history"].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        data["last_query"] = query
        data["last_answer"] = answer

        if query and query not in data["topics"]:

            data["topics"].append(
                query
            )

        if summary is not None:

            data["summary"] = summary

        if keywords:

            for keyword in keywords:

                if keyword not in data["keywords"]:

                    data["keywords"].append(
                        keyword
                    )

        if sources:

            for source in sources:

                if source not in data["sources"]:

                    data["sources"].append(
                        source
                    )

        if notes:

            for note in notes:

                if note not in data["notes"]:

                    data["notes"].append(
                        note
                    )

        if timeline:

            data["timeline"] = timeline

        if research_state is not None:

            data["research_state"] = research_state

        data["updated_at"] = (
            datetime.utcnow().isoformat()
        )

        self._file(
            session_id
        ).write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return data