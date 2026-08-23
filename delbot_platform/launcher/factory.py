from __future__ import annotations

from delbot_platform.core.lifecycle.service_definition import (
    ServiceDefinition,
)

from delbot_platform.launcher.base import (
    BaseLauncher,
)

from delbot_platform.launcher.ai_runtime import (
    AIRuntimeLauncher,
)

from delbot_platform.launcher.gateway_launcher import (
    GatewayLauncher,
)

from delbot_platform.launcher.paddleocr import (
    PaddleOCRLauncher,
)

from delbot_platform.launcher.research_api_launcher import (
    ResearchAPILauncher,
)

from delbot_platform.launcher.whisper import (
    WhisperLauncher,
)


class LauncherFactory:

    _LAUNCHERS = {

        "gateway": GatewayLauncher,

        "research_api": ResearchAPILauncher,

        "chat": AIRuntimeLauncher,

        "embedding": AIRuntimeLauncher,

        "reranker": AIRuntimeLauncher,

        "vision": AIRuntimeLauncher,

        "ocr": PaddleOCRLauncher,

        "speech": WhisperLauncher,

    }

    @classmethod
    def create(
        cls,
        definition: ServiceDefinition,
    ) -> BaseLauncher:

        launcher = cls._LAUNCHERS.get(
            definition.launcher,
        )

        if launcher is None:

            raise ValueError(
                f"Unknown launcher: {definition.launcher}"
            )

        return launcher()
