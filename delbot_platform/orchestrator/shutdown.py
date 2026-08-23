from __future__ import annotations

from delbot_platform.controller.service_controller import (
    ServiceController,
)

from delbot_platform.core.lifecycle.orchestrator import (
    PlatformOrchestrator,
)


class ShutdownOrchestrator:

    def __init__(self) -> None:

        self.platform = PlatformOrchestrator()

        self.controller = ServiceController()

    def shutdown(self) -> dict[str, bool]:

        results: dict[str, bool] = {}

        #
        # stop in reverse registration order
        #

        services = list(
            self.platform.definitions()
        )

        services.reverse()

        for service in services:

            try:

                results[
                    service.name
                ] = self.controller.stop(
                    service.name,
                )

            except Exception:

                results[
                    service.name
                ] = False

        return results
