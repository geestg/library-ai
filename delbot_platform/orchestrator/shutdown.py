from __future__ import annotations

from delbot_platform.controller.service_controller import (
    ServiceController,
)
from delbot_platform.services.service_registry import (
    PlatformServiceRegistry,
)


class ShutdownOrchestrator:

    def __init__(self) -> None:

        self.registry = PlatformServiceRegistry()

        self.controller = ServiceController()

    def shutdown(self) -> dict[str, bool]:

        results: dict[str, bool] = {}

        #
        # Reverse order
        #

        services = list(
            self.registry.enabled()
        )

        services.reverse()

        for service in services:

            results[service.name] = (
                self.controller.stop(
                    service.name,
                )
            )

        return results

    def run(self) -> None:

        print()

        print("===================================")
        print("DELBot Platform Shutdown")
        print("===================================")

        print()

        results = self.shutdown()

        if not results:

            print("No services registered.")
            print()

            return

        for name, stopped in results.items():

            status = (
                "STOPPED"
                if stopped
                else "NOT RUNNING"
            )

            print(
                f"{name:<15}{status}"
            )

        print()