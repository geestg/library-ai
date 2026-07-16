from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.boot.boot_state import (
    BootState,
)


@dataclass(slots=True)
class BootResult:

    service: str

    state: BootState

    pid: int | None = None

    host: str = ""

    port: int = 0

    elapsed: float = 0.0

    message: str = ""

    @property
    def ready(self) -> bool:

        return self.state is BootState.READY

    @property
    def failed(self) -> bool:

        return self.state in (
            BootState.FAILED,
            BootState.TIMEOUT,
        )