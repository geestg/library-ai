from __future__ import annotations

from enum import Enum


class BootState(str, Enum):

    BOOTING = "BOOTING"

    WAITING_PROCESS = "WAITING_PROCESS"

    WAITING_HEALTH = "WAITING_HEALTH"

    READY = "READY"

    FAILED = "FAILED"

    TIMEOUT = "TIMEOUT"