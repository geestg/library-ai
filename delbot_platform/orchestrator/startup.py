from __future__ import annotations

from delbot_platform.boot.service_boot import (
    ServiceBoot,
)

from delbot_platform.controller.service_controller import (
    ServiceController,
)


class StartupOrchestrator:

    def __init__(self) -> None:

        self.controller = ServiceController()

        self.boot = ServiceBoot()


    ###########################################################################
    # Start Platform
    ###########################################################################

    def run(self):

        print()

        print("=" * 70)
        print("DELBot Platform Startup")
        print("=" * 70)

        processes = self.boot.boot()

        print()

        print("=" * 70)
        print("Startup Completed")
        print("=" * 70)

        for process in processes:

            print(
                f"{process.name:20}"
                f"PID={process.pid}"
            )

        return processes


    ###########################################################################
    # Stop Platform
    ###########################################################################

    def stop(self):

        print()

        print("=" * 70)
        print("Stopping DELBot Platform")
        print("=" * 70)

        return self.controller.stop_all()
