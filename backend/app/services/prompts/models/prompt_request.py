from dataclasses import dataclass
from dataclasses import field

from app.services.llm.models.execution_config import (
    ExecutionConfig,
)

from .prompt_type import PromptType


@dataclass(slots=True)
class PromptRequest:

    prompt: str

    prompt_type: PromptType = field(
        default=PromptType.ANSWER
    )

    execution: ExecutionConfig = field(
        default_factory=ExecutionConfig
    )

    model: str | None = None

    provider: str | None = None

    # =====================================
    # INTERNAL FACTORY
    # =====================================

    @classmethod
    def _create(
        cls,
        *,
        prompt: str,
        prompt_type: PromptType,
        execution: ExecutionConfig,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls(

            prompt=prompt,

            prompt_type=prompt_type,

            execution=execution,

            model=model,

            provider=provider,

        )

    # =====================================
    # ANSWER
    # =====================================

    @classmethod
    def answer(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.ANSWER,

            execution=ExecutionConfig(
                temperature=0,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # DOCUMENT
    # =====================================

    @classmethod
    def document(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.DOCUMENT,

            execution=ExecutionConfig(
                temperature=0,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # VERIFIER
    # =====================================

    @classmethod
    def verifier(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.VERIFIER,

            execution=ExecutionConfig(
                temperature=0,
                max_tokens=8,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # QUERY RESOLUTION
    # =====================================

    @classmethod
    def query_resolution(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.QUERY_RESOLUTION,

            execution=ExecutionConfig(
                temperature=0,
                max_tokens=32,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # RESEARCH
    # =====================================

    @classmethod
    def research(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.RESEARCH,

            execution=ExecutionConfig(
                temperature=0.2,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # CREATIVE
    # =====================================

    @classmethod
    def creative(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.CREATIVE,

            execution=ExecutionConfig(
                temperature=0.7,
            ),

            model=model,

            provider=provider,

        )

    # =====================================
    # TITLE
    # =====================================

    @classmethod
    def title(
        cls,
        prompt: str,
        *,
        model: str | None = None,
        provider: str | None = None,
    ) -> "PromptRequest":

        return cls._create(

            prompt=prompt,

            prompt_type=PromptType.TITLE,

            execution=ExecutionConfig(
                temperature=0.3,
                max_tokens=32,
            ),

            model=model,

            provider=provider,

        )