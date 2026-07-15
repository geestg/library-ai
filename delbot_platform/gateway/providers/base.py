from abc import ABC
from abc import abstractmethod

from delbot_platform.gateway.schemas.request import ChatRequest
from delbot_platform.gateway.schemas.response import ChatResponse


class BaseProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        pass