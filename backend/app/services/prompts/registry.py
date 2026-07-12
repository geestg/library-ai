from collections.abc import Callable

from app.services.prompts.models.prompt_type import (
    PromptType,
)


class PromptRegistry:

    _builders: dict[
        PromptType,
        Callable,
    ] = {}

    @classmethod
    def register(
        cls,
        prompt_type: PromptType,
        builder: Callable,
    ) -> None:

        cls._builders[prompt_type] = builder

    @classmethod
    def build(
        cls,
        prompt_type: PromptType,
        **kwargs,
    ) -> str:

        builder = cls._builders[prompt_type]

        return builder.build(
            **kwargs
        )

    @classmethod
    def get(
        cls,
        prompt_type: PromptType,
    ):

        return cls._builders[prompt_type]