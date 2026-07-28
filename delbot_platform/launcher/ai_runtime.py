from __future__ import annotations

from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)

from delbot_platform.core.lifecycle.service_definition import (
    ServiceDefinition,
)

from delbot_platform.core.path_manager import (
    PathManager,
)

from delbot_platform.launcher.base import (
    BaseLauncher,
)

from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class AIRuntimeLauncher(BaseLauncher):

    HEALTH_ENDPOINT = "/health"

    CATEGORY_MAP = {
        "chat": "chat",
        "embedding": "embedding",
        "reranker": "reranker",
        "vision": "vision",
        "ocr": "ocr",
    }

    def __init__(self) -> None:

        self.registry = ModelRegistry()

    def build(
        self,
        definition: ServiceDefinition,
    ) -> LaunchSpec:

        category = self.CATEGORY_MAP.get(
            definition.name,
        )

        if category is None:

            raise ValueError(
                f"Unsupported AI runtime: {definition.name}"
            )

        model = self.registry.default(
            category,
        )

        module = (
            f"delbot_platform.ai.runtime.{definition.name}"
        )

        return LaunchSpec(
            name=definition.name,
            command=[
                "python",
                "-m",
                module,
            ],
            workdir=PathManager.ROOT,
            host=model.runtime.host,
            port=model.runtime.port,
            health_check=True,
            health_endpoint=self.HEALTH_ENDPOINT,
            environment=None,
        )
