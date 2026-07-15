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


class VLLMLauncher(BaseLauncher):

    NAME = "chat"

    HOST = "127.0.0.1"

    PORT = 8101

    HEALTH_ENDPOINT = "/health"

    MODULE = "delbot_platform.ai.runtime.chat"

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