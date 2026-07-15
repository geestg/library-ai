from __future__ import annotations

from delbot_platform.launcher.vllm import (
    VLLMLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class VisionService(PlatformService):

    @property
    def name(self) -> str:

        return "vision"

    def launcher(
        self,
    ) -> VLLMLauncher:

        return VLLMLauncher()