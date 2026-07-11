from dataclasses import dataclass

from .prompt_type import (
    PromptType,
)


@dataclass(slots=True)
class PromptRequest:

    prompt: str

    prompt_type: PromptType

    model: str | None = None

    provider: str | None = None