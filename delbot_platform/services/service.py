from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.core.service_registry import (
    Service,
)

from delbot_platform.core.service_registry import (
    ServiceRegistry,
)

from delbot_platform.launcher.base import (
    BaseLauncher,
)

from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class PlatformService(ABC):
    """
    Base abstraction describing an AI Platform service.

    PlatformService only describes the service identity and
    provides configuration from ServiceRegistry.

    Runtime lifecycle is handled by ServiceBoot and
    ProcessManager.
    """

    def __init__(self) -> None:

        self._registry = ServiceRegistry()

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def config(self) -> Service:

        return self._registry.get(
            self.name,
        )

    @property
    def host(self) -> str:

        return self.config.host

    @property
    def port(self) -> int:

        return self.config.port

    @property
    def enabled(self) -> bool:

        return self.config.enabled

    @abstractmethod
    def launcher(
        self,
    ) -> BaseLauncher:
        ...

    def launch_spec(
        self,
    ) -> LaunchSpec:

        return self.launcher().build()