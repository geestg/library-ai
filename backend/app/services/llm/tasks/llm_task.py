from app.services.llm.model_gateway import (
    gateway,
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

        return gateway.generate_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **request.execution.to_kwargs(),

        )

    # =====================================
    # STREAM
    # =====================================

    @staticmethod
    def stream(
        request: PromptRequest,
    ):

        return gateway.stream_response(

            prompt=request.prompt,

            model=request.model,

            provider=request.provider,

            **request.execution.to_kwargs(),

        )