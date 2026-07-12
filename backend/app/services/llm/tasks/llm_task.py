from app.services.llm.model_gateway import (
    gateway,
)

from app.services.llm.generation_profiles import (
    GenerationProfiles,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)


class LLMTask:

    # =====================================
    # ANSWER
    # =====================================

    @staticmethod
    def answer(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.ANSWER,

        )

    # =====================================
    # STREAM ANSWER
    # =====================================

    @staticmethod
    def stream_answer(
        request: PromptRequest,
    ):

        return gateway.stream_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.ANSWER,

        )

    # =====================================
    # VERIFIER
    # =====================================

    @staticmethod
    def verifier(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.VERIFIER,

        )

    # =====================================
    # QUERY RESOLUTION
    # =====================================

    @staticmethod
    def query_resolution(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.QUERY_RESOLUTION,

        )

    # =====================================
    # TITLE
    # =====================================

    @staticmethod
    def title(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.TITLE,

        )

    # =====================================
    # RESEARCH
    # =====================================

    @staticmethod
    def research(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.RESEARCH,

        )

    # =====================================
    # CREATIVE
    # =====================================

    @staticmethod
    def creative(
        request: PromptRequest,
    ):

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **GenerationProfiles.CREATIVE,

        )

