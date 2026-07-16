from __future__ import annotations

from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)
from delbot_platform.boot.boot_result import (
    BootResult,
)
from delbot_platform.boot.boot_state import (
    BootState,
)
from delbot_platform.boot.service_boot import (
    ServiceBoot,
)
from delbot_platform.services.service_registry import (
    PlatformServiceRegistry,
)


class ServiceController:

    def __init__(self) -> None:

        self.registry = PlatformServiceRegistry()

        self.boot = ServiceBoot()

        self.process = ProcessManager()

    #
    # Single service
    #

    def start(
        self,
        name: str,
    ) -> BootResult:

        service = self.registry.get(
            name,
        )

        spec = service.launch_spec()

        return self.boot.start(
            spec,
        )

    def stop(
        self,
        name: str,
    ) -> bool:

        return self.process.stop(
            name,
        )

    #
    # Batch
    #

    def start_all(
        self,
    ) -> list[BootResult]:

        results: list[BootResult] = []

        for service in self.registry.enabled():

            try:

                result = self.start(
                    service.name,
                )

            except Exception as exc:

                result = BootResult(
                    service=service.name,
                    state=BootState.FAILED,
                    message=str(exc),
                )

            results.append(
                result,
            )

        return results

    def stop_all(
        self,
    ) -> dict[str, bool]:

        results: dict[str, bool] = {}

        for service in self.registry.enabled():

            try:

                results[
                    service.name
                ] = self.stop(
                    service.name,
                )

            except Exception:

                results[
                    service.name
                ] = False

        return results