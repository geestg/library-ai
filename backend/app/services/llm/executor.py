from app.services.llm.generation_profiles import (
    GenerationProfiles,
)

from app.services.llm.model_gateway import (
    gateway,
)


class LLMExecutor:

    # =====================================
    # ANSWER
    # =====================================

    @staticmethod
    def answer(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.ANSWER,

        )

    # =====================================
    # STREAM ANSWER
    # =====================================

    @staticmethod
    def stream_answer(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.stream_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.ANSWER,

        )

    # =====================================
    # VERIFIER
    # =====================================

    @staticmethod
    def verifier(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.VERIFIER,

        )

    # =====================================
    # QUERY RESOLUTION
    # =====================================

    @staticmethod
    def query_resolution(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.QUERY_RESOLUTION,

        )

    # =====================================
    # TITLE
    # =====================================

    @staticmethod
    def title(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.TITLE,

        )

    # =====================================
    # RESEARCH
    # =====================================

    @staticmethod
    def research(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.RESEARCH,

        )

    # =====================================
    # CREATIVE
    # =====================================

    @staticmethod
    def creative(
        prompt: str,
        model: str | None = None,
        provider: str | None = None,
    ):

        return gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

            **GenerationProfiles.CREATIVE,

        )
