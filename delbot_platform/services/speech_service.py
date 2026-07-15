from __future__ import annotations

from delbot_platform.launcher.whisper import (
    WhisperLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class SpeechService(PlatformService):

    @property
    def name(self) -> str:

        return "speech"

    def launcher(
        self,
    ) -> WhisperLauncher:

        return WhisperLauncher()