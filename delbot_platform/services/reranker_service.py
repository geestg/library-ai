from __future__ import annotations

from delbot_platform.launcher.infinity import (
    InfinityLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class RerankerService(PlatformService):

    @property
    def name(self) -> str:

        return "reranker"

    def launcher(
        self,
    ) -> InfinityLauncher:

        return InfinityLauncher()