from __future__ import annotations

from delbot_platform.core.service_registry import (
    Service,
)

from delbot_platform.launcher.base import (
    BaseLauncher,
)

from delbot_platform.launcher.gateway_launcher import (
    GatewayLauncher,
)

from delbot_platform.launcher.infinity import (
    InfinityLauncher,
)

from delbot_platform.launcher.paddleocr import (
    PaddleOCRLauncher,
)

from delbot_platform.launcher.research_api_launcher import (
    ResearchAPILauncher,
)

from delbot_platform.launcher.vllm import (
    VLLMLauncher,
)

from delbot_platform.launcher.whisper import (
    WhisperLauncher,
)


class LauncherFactory:

    _LAUNCHERS = {

        "gateway": GatewayLauncher,

        "research_api": ResearchAPILauncher,

        "chat": VLLMLauncher,

        "embedding": InfinityLauncher,

        "reranker": InfinityLauncher,

        "vision": VLLMLauncher,

        "ocr": PaddleOCRLauncher,

        "speech": WhisperLauncher,

    }

    #
    # Production API
    #

    @classmethod
    def create(
        cls,
        service: Service,
    ) -> BaseLauncher:

        launcher = cls._LAUNCHERS.get(
            service.name,
        )

        if launcher is None:

            raise ValueError(
                f"No launcher registered for '{service.name}'."
            )

        return launcher()

    #
    # Backward Compatibility
    #

    @staticmethod
    def gateway() -> GatewayLauncher:

        return GatewayLauncher()

    @staticmethod
    def research_api() -> ResearchAPILauncher:

        return ResearchAPILauncher()

    @staticmethod
    def embedding() -> InfinityLauncher:

        return InfinityLauncher()

    @staticmethod
    def reranker() -> InfinityLauncher:

        return InfinityLauncher()

    @staticmethod
    def vision() -> VLLMLauncher:

        return VLLMLauncher()

    @staticmethod
    def ocr() -> PaddleOCRLauncher:

        return PaddleOCRLauncher()

    @staticmethod
    def speech() -> WhisperLauncher:

        return WhisperLauncher()