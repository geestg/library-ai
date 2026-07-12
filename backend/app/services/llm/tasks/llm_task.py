from app.services.llm.model_gateway import (
    gateway,
)

from app.services.llm.generation_profile_resolver import (
    GenerationProfileResolver,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)


class LLMTask:

    # =====================================
    # EXECUTE
    # =====================================

    @staticmethod
    def execute(
        request: PromptRequest,
    ):

        config = request.execution

        if config == config.__class__():

            config = (
                GenerationProfileResolver.resolve(
                    request.prompt_type
                )
            )

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **config.to_kwargs(),

        )

    # =====================================
    # STREAM
    # =====================================

    @staticmethod
    def stream(
        request: PromptRequest,
    ):

        config = request.execution

        if config == config.__class__():

            config = (
                GenerationProfileResolver.resolve(
                    request.prompt_type
                )
            )

        return gateway.stream_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **config.to_kwargs(),

        )