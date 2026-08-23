from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from delbot_platform.research.models import Citation


class ResearchState:
    """
    Menyimpan state penelitian untuk satu Workspace.

    State internal menggunakan object Python.
    export() menghasilkan struktur JSON-safe.
    """

    def __init__(
        self,
        initial: dict[str, Any] | None = None,
    ) -> None:

        now = datetime.utcnow().isoformat()

        self.state: dict[str, Any] = {
            "topic": None,
            "research_goal": None,
            "current_question": None,
            "current_answer": None,
            "summary": "",
            "keywords": [],
            "sources": [],
            "notes": [],
            "timeline": [],
            "created_at": now,
            "updated_at": now,
        }

        if initial:

            data = deepcopy(initial)

            sources = []

            for source in data.get(
                "sources",
                [],
            ):

                if isinstance(
                    source,
                    Citation,
                ):

                    sources.append(source)

                else:

                    sources.append(
                        Citation.from_dict(
                            source
                        )
                    )

            data["sources"] = sources

            self.state.update(data)

    def touch(self) -> None:

        self.state["updated_at"] = (
            datetime.utcnow().isoformat()
        )

    def update(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.state[key] = value
        self.touch()

    def update_topic(
        self,
        topic: str,
    ) -> None:

        self.state["topic"] = topic
        self.touch()

    def update_goal(
        self,
        goal: str,
    ) -> None:

        self.state["research_goal"] = goal
        self.touch()

    def update_summary(
        self,
        summary: str,
    ) -> None:

        self.state["summary"] = summary
        self.touch()

    def update_question(
        self,
        question: str,
    ) -> None:

        self.state["current_question"] = question

        self.add_timeline(
            "question",
            question,
        )

        self.touch()

    def update_answer(
        self,
        answer: str,
    ) -> None:

        self.state["current_answer"] = answer

        self.add_timeline(
            "answer",
            answer,
        )

        self.touch()

    def add_keyword(
        self,
        keyword: str,
    ) -> None:

        keyword = keyword.strip()

        if (
            keyword
            and keyword not in self.state["keywords"]
        ):

            self.state["keywords"].append(
                keyword
            )

            self.touch()

    def add_source(
        self,
        source: Citation,
    ) -> None:

        exists = any(
            item.chunk_id == source.chunk_id
            for item in self.state["sources"]
        )

        if not exists:

            self.state["sources"].append(
                source
            )

            self.touch()

    def add_note(
        self,
        note: str,
    ) -> None:

        note = note.strip()

        if note:

            self.state["notes"].append(
                note
            )

            self.touch()

    def add_timeline(
        self,
        event: str,
        value: Any,
    ) -> None:

        self.state["timeline"].append(
            {
                "time": datetime.utcnow().isoformat(),
                "event": event,
                "value": value,
            }
        )

    @property
    def sources(
        self,
    ) -> list[Citation]:

        return list(
            self.state["sources"]
        )

    def export(
        self,
    ) -> dict[str, Any]:

        data = deepcopy(
            self.state
        )

        data["sources"] = [
            source.export()
            for source in self.state["sources"]
        ]

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ResearchState":

        return cls(
            initial=data,
        )