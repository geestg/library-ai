from __future__ import annotations

from delbot_platform.core.service_registry import (
    ServiceRegistry,
)

from delbot_platform.services.chat_service import (
    ChatService,
)

from delbot_platform.services.embedding_service import (
    EmbeddingService,
)

from delbot_platform.services.gateway_service import (
    GatewayService,
)

from delbot_platform.services.ocr_service import (
    OCRService,
)

from delbot_platform.services.reranker_service import (
    RerankerService,
)

from delbot_platform.services.research_api_service import (
    ResearchAPIService,
)

from delbot_platform.services.service import (
    PlatformService,
)

from delbot_platform.services.speech_service import (
    SpeechService,
)

from delbot_platform.services.vision_service import (
    VisionService,
)


class PlatformServiceRegistry:
    """
    Converts configuration-defined services into PlatformService
    implementations.

    Configuration remains the source of truth.
    """

    _SERVICES: dict[str, type[PlatformService]] = {

        "gateway": GatewayService,

        "research_api": ResearchAPIService,

        "chat": ChatService,

        "embedding": EmbeddingService,

        "reranker": RerankerService,

        "vision": VisionService,

        "ocr": OCRService,

        "speech": SpeechService,

    }

    def __init__(self) -> None:

        self._registry = ServiceRegistry()

        self._services: dict[str, PlatformService] = {}

        for config in self._registry.enabled():

            service_cls = self._SERVICES.get(
                config.name,
            )

            if service_cls is None:
                continue

            self._services[
                config.name
            ] = service_cls()

    #
    # Backward Compatibility
    #

    def service(
        self,
        name: str,
    ) -> PlatformService:

        return self.get(
            name,
        )

    def all(
        self,
    ) -> list[PlatformService]:

        return self.services()

    #
    # Current API
    #

    def get(
        self,
        name: str,
    ) -> PlatformService:

        return self._services[
            name
        ]

    def services(
        self,
    ) -> list[PlatformService]:

        return list(
            self._services.values()
        )

    def enabled(
        self,
    ) -> list[PlatformService]:

        return self.services()

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._services

    #
    # Python API
    #

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(
            name,
        )

    def __iter__(
        self,
    ):

        return iter(
            self._services.values()
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._services
        )