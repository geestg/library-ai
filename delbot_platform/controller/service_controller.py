from __future__ import annotations

from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)
from delbot_platform.boot.service_boot import (
    ServiceBoot,
)
from delbot_platform.services.service_registry import (
    PlatformServiceRegistry,
)


class ServiceController:
    """
    Facade responsible for managing the lifecycle of AI Platform services.

    The controller coordinates PlatformService definitions,
    ServiceBoot, and ProcessManager without exposing runtime
    implementation details to callers.
    """

    def __init__(self) -> None:

        self.registry = PlatformServiceRegistry()

        self.boot = ServiceBoot()

        self.process = ProcessManager()

    #
    # Single service operations
    #

    def start(
        self,
        name: str,
    ):

        service = self.registry.get(name)

        spec = service.launch_spec()

        return self.boot.start(spec)

    def stop(
        self,
        name: str,
    ) -> bool:

        return self.process.stop(name)

    #
    # Batch operations
    #

    def start_all(self):

        processes = []

        for service in self.registry.enabled():

            processes.append(
                self.start(
                    service.name,
                )
            )

        return processes

    def stop_all(self):

        results = {}

        for service in self.registry.enabled():

            results[service.name] = self.stop(
                service.name,
            )

        return results