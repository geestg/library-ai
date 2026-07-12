from collections.abc import Callable

from app.services.prompts.models.prompt_type import (
    PromptType,
)


class PromptRegistry:

    _builders: dict[
        PromptType,
        Callable,
    ] = {}

    # =====================================
    # REGISTER
    # =====================================

    @classmethod
    def register(
        cls,
        prompt_type: PromptType,
        builder: Callable,
    ) -> None:

        if prompt_type in cls._builders:

            raise ValueError(

                f"Prompt '{prompt_type.value}' "
                "is already registered."

            )

        cls._builders[
            prompt_type
        ] = builder

    # =====================================
    # BUILD
    # =====================================

    @classmethod
    def build(
        cls,
        prompt_type: PromptType,
        **kwargs,
    ) -> str:

        if not cls.has(
            prompt_type
        ):

            raise ValueError(

                f"No prompt builder registered "
                f"for '{prompt_type.value}'."

            )

        builder = cls._builders[
            prompt_type
        ]

        return builder.build(
            **kwargs
        )

    # =====================================
    # GET BUILDER
    # =====================================

    @classmethod
    def get(
        cls,
        prompt_type: PromptType,
    ):

        if not cls.has(
            prompt_type
        ):

            raise ValueError(

                f"No prompt builder registered "
                f"for '{prompt_type.value}'."

            )

        return cls._builders[
            prompt_type
        ]

    # =====================================
    # HAS
    # =====================================

    @classmethod
    def has(
        cls,
        prompt_type: PromptType,
    ) -> bool:

        return (
            prompt_type
            in
            cls._builders
        )

    # =====================================
    # LIST REGISTERED TYPES
    # =====================================

    @classmethod
    def registered_types(
        cls,
    ) -> list[PromptType]:

        return list(
            cls._builders.keys()
        )

    # =====================================
    # CLEAR
    # =====================================

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._builders.clear()