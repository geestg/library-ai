from __future__ import annotations

from delbot_platform.launcher.paddleocr import (
    PaddleOCRLauncher,
)

from delbot_platform.services.service import (
    PlatformService,
)


class OCRService(PlatformService):

    @property
    def name(self) -> str:

        return "ocr"

    def launcher(
        self,
    ) -> PaddleOCRLauncher:

        return PaddleOCRLauncher()