from __future__ import annotations

import time

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class ChatCompletionMessage:

    role: str

    content: str


@dataclass(slots=True)
class ChatCompletionChoice:

    index: int

    message: ChatCompletionMessage

    finish_reason: str = "stop"


@dataclass(slots=True)
class ChatCompletionResponse:

    model: str

    choices: list[ChatCompletionChoice]

    id: str = "chatcmpl-delbot"

    object: str = "chat.completion"

    created: int = field(
        default_factory=lambda: int(time.time()),
    )