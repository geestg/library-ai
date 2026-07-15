from delbot_platform.gateway.providers.base import BaseProvider
from delbot_platform.gateway.schemas.request import ChatRequest
from delbot_platform.gateway.schemas.response import ChatResponse


class LocalProvider(BaseProvider):

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        return ChatResponse(
            model=request.model,
            response="Dummy response from LocalProvider",
        )