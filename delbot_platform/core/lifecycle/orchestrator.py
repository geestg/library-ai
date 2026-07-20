"""
DELBot Platform Orchestrator.

Coordinates lifecycle operations for managed platform services.
"""

from __future__ import annotations

from abc import ABC
from typing import Protocol

from .boot_policy import BootPolicy
from .service_dependency import ServiceDependency
from .service_state import ServiceState


class ServiceHandle(Protocol):
    """
    Minimal interface exposed by a managed service.
    """

    @property
    def name(self) -> str: ...

    @property
    def state(self) -> ServiceState: ...


class PlatformOrchestrator(ABC):
    """
    Base lifecycle orchestrator.

    Concrete implementations integrate with RuntimeLauncher,
    ProcessManager and RecoveryManager.
    """

    def start(self, service: ServiceHandle) -> None:
        raise NotImplementedError

    def stop(self, service: ServiceHandle) -> None:
        raise NotImplementedError

    def restart(self, service: ServiceHandle) -> None:
        raise NotImplementedError

    def recover(self, service: ServiceHandle) -> None:
        raise NotImplementedError

    def health(self, service: ServiceHandle) -> bool:
        raise NotImplementedError
