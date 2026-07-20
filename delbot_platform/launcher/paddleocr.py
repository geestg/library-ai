from __future__ import annotations

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


class PaddleOCRLauncher(BaseLauncher):

    MODULE = "delbot_platform.ai.runtime.ocr"

    HEALTH_ENDPOINT = "/health"

    def build(
        self,
        definition: ServiceDefinition,
    ) -> LaunchSpec:

        return LaunchSpec(
            name=definition.name,
            command=[
                "python",
                "-m",
                self.MODULE,
            ],
            workdir=PathManager.ROOT,
            host=definition.host,
            port=definition.port,
            health_check=True,
            health_endpoint=self.HEALTH_ENDPOINT,
            environment=None,
        )
