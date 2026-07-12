from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ExecutionConfig:

    temperature: float = 0.0

    max_tokens: int | None = None

    def to_kwargs(self) -> dict:

        kwargs = {
            "temperature": self.temperature,
        }

        if self.max_tokens is not None:

            kwargs["max_tokens"] = self.max_tokens

        return kwargs