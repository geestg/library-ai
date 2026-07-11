from dataclasses import dataclass, field

from .prompt_type import PromptType


@dataclass(slots=True)
class PromptRequest:

    prompt: str

    prompt_type: PromptType = field(
        default=PromptType.ANSWER
    )

    model: str | None = None

    provider: str | None = None
