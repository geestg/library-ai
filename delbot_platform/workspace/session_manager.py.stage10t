from __future__ import annotations

import json
import uuid

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from delbot_platform.research.state.research_state import ResearchState


class SessionManager:

    def __init__(self) -> None:

        self.base_path = Path("runtime/workspace")

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.sessions: dict[str, dict[str, Any]] = {}

        self.load_all()

    def _file(
        self,
        session_id: str,
    ) -> Path:

        return self.base_path / f"{session_id}.json"

    def load_all(self) -> None:

        self.sessions.clear()

        for file in self.base_path.glob("*.json"):

            try:

                session = json.loads(
                    file.read_text(
                        encoding="utf-8",
                    )
                )

                self.sessions[
                    session["session_id"]
                ] = session

            except Exception:
                continue

    def save(
        self,
        session: dict[str, Any],
    ) -> None:

        session["updated_at"] = (
            datetime.utcnow().isoformat()
        )

        self._file(
            session["session_id"]
        ).write_text(
            json.dumps(
                session,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create(
        self,
        title: str,
    ) -> dict[str, Any]:

        session_id = str(
            uuid.uuid4()
        )

        state = ResearchState()

        state.update_topic(title)

        now = datetime.utcnow().isoformat()

        session = {
            "session_id": session_id,
            "title": title,
            "messages": [],
            "metadata": {},
            "research_state": state.export(),
            "created_at": now,
            "updated_at": now,
        }

        self.sessions[
            session_id
        ] = session

        self.save(session)

        return deepcopy(session)

    def get(
        self,
        session_id: str,
    ) -> dict[str, Any] | None:

        session = self.sessions.get(session_id)

        if session is None:
            return None

        return session

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return session_id in self.sessions

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> dict[str, Any] | None:

        session = self.get(session_id)

        if session is None:
            return None

        session["messages"].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        self.save(session)

        return session

    def update_state(
        self,
        session_id: str,
        key: str,
        value: Any,
    ) -> dict[str, Any] | None:

        session = self.get(session_id)

        if session is None:
            return None

        session["research_state"][key] = value

        self.save(session)

        return session

    def replace_state(
        self,
        session_id: str,
        state: ResearchState,
    ) -> dict[str, Any] | None:

        session = self.get(session_id)

        if session is None:
            return None

        session["research_state"] = state.export()

        self.save(session)

        return session

    def get_state(
        self,
        session_id: str,
    ) -> ResearchState | None:

        session = self.get(session_id)

        if session is None:
            return None

        return ResearchState.from_dict(
            session["research_state"]
        )