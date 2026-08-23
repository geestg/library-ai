from __future__ import annotations

from delbot_platform.gateway.providers.base import (
    BaseProvider,
)
from delbot_platform.gateway.request import (
    ChatRequest,
)
from delbot_platform.gateway.response import (
    ChatResponse,
)


class LocalProvider(BaseProvider):

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        return ChatResponse(
            content="Dummy response from LocalProvider",
            model=request.model or "local",
        )