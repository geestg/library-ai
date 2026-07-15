from __future__ import annotations

from delbot_platform.launcher.infinity import (
    InfinityLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class EmbeddingService(PlatformService):

    @property
    def name(self) -> str:

        return "embedding"

    def launcher(
        self,
    ) -> InfinityLauncher:

        return InfinityLauncher()