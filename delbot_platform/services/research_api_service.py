from __future__ import annotations

from delbot_platform.launcher.research_api_launcher import (
    ResearchAPILauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class ResearchAPIService(PlatformService):

    @property
    def name(self) -> str:

        return "research_api"

    def launcher(
        self,
    ) -> ResearchAPILauncher:

        return ResearchAPILauncher()