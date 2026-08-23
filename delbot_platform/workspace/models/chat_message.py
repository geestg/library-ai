from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChatMessage:

    role: str

    content: str

    timestamp: str

    def export(
        self,
    ) -> dict[str, str]:

        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ChatMessage":

        return cls(
            role=data.get(
                "role",
                "",
            ),
            content=data.get(
                "content",
                "",
            ),
            timestamp=data.get(
                "timestamp",
                "",
            ),
        )