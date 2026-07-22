from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


class ResearchState:
    """
    Menyimpan state penelitian aktif untuk satu Research Session.

    State ini digunakan oleh Workspace, Prompt Builder,
    Research Engine, dan Memory sehingga seluruh proses
    penelitian mempunyai konteks yang konsisten.
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
            "created_at": now,
            "updated_at": now,
        }

        if initial:
            self.state.update(initial)

    def touch(self) -> None:
        self.state["updated_at"] = datetime.utcnow().isoformat()

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
        self.touch()

    def update_answer(
        self,
        answer: str,
    ) -> None:

        self.state["current_answer"] = answer
        self.touch()

    def add_keyword(
        self,
        keyword: str,
    ) -> None:

        keyword = keyword.strip()

        if keyword and keyword not in self.state["keywords"]:
            self.state["keywords"].append(keyword)
            self.touch()

    def add_source(
        self,
        source: Any,
    ) -> None:

        if source not in self.state["sources"]:
            self.state["sources"].append(source)
            self.touch()

    def add_note(
        self,
        note: str,
    ) -> None:

        note = note.strip()

        if note:
            self.state["notes"].append(note)
            self.touch()

    def export(self) -> dict[str, Any]:
        return deepcopy(self.state)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ResearchState":
        return cls(initial=data)