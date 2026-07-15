from __future__ import annotations

from delbot_platform.launcher.vllm import (
    VLLMLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class ChatService(PlatformService):

    @property
    def name(self) -> str:

        return "chat"

    def launcher(
        self,
    ) -> VLLMLauncher:

        return VLLMLauncher()