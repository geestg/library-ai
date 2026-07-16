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


class ResearchAPILauncher(BaseLauncher):

    NAME = "research_api"

    HOST = "127.0.0.1"

    PORT = 8200

    HEALTH_ENDPOINT = "/"

    def build(
        self,
    ) -> LaunchSpec:

        return LaunchSpec(

            name=self.NAME,

            command=[
                "python",
                "-m",
                "delbot_platform.api",
            ],

            workdir=PathManager.ROOT,

            host=self.HOST,

            port=self.PORT,

            health_check=True,

            health_endpoint=self.HEALTH_ENDPOINT,

            environment=None,
        )