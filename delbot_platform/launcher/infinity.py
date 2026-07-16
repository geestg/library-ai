from __future__ import annotations

from delbot_platform.core.path_manager import (
    PathManager,
)
from delbot_platform.launcher.base import (
    BaseLauncher,
)
from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class InfinityLauncher(BaseLauncher):

    NAME = "embedding"

    HOST = "127.0.0.1"

    PORT = 8102

    HEALTH_ENDPOINT = "/health"

    MODULE = "delbot_platform.ai.runtime.embedding"

    def build(self) -> LaunchSpec:

        return LaunchSpec(
            name=self.NAME,
            command=[
                "python",
                "-m",
                self.MODULE,
            ],
            workdir=PathManager.ROOT,
            host=self.HOST,
            port=self.PORT,
            health_check=True,
            health_endpoint=self.HEALTH_ENDPOINT,
            environment=None,
        )