from __future__ import annotations

from delbot_platform.ai.recovery.recovery import (
    RecoveryManager,
)
from delbot_platform.boot.boot_result import (
    BootResult,
)
from delbot_platform.boot.boot_state import (
    BootState,
)
from delbot_platform.controller.service_controller import (
    ServiceController,
)
from delbot_platform.core.config_manager import (
    ConfigManager,
)
from delbot_platform.core.environment import (
    EnvironmentManager,
)
from delbot_platform.core.runtime_manager import (
    RuntimeManager,
)


class StartupOrchestrator:

    def __init__(self) -> None:

        self.config = ConfigManager()

        self.controller = ServiceController()

    #
    # Initialization
    #

    def initialize(self) -> None:

        EnvironmentManager.setup()

        RuntimeManager.ensure_directories()

    def recover(self):

        return RecoveryManager.load_states()

    #
    # Startup
    #

    def start_services(
        self,
    ) -> list[BootResult]:

        return self.controller.start_all()

    #
    # UI
    #

    def _print_results(
        self,
        results: list[BootResult],
    ) -> None:

        if not results:

            print("No services configured.")
            return

        print()

        print("Service Startup Results")
        print("-----------------------")

        for result in results:

            elapsed = f"{result.elapsed:.2f}s"

            print(
                f"{result.service:<12}"
                f"{result.state.value:<12}"
                f"{elapsed:<10}"
                f"{result.message}"
            )

    #
    # Main
    #

    def run(self) -> list[BootResult]:

        print()

        print("===================================")
        print("DELBot Platform")
        print("===================================")

        print()

        print("Initializing environment...")

        self.initialize()

        print("Environment OK")

        print()

        print("Recovering services...")

        states = self.recover()

        if not states:

            print("No previous services found.")

        else:

            for state in states:

                status = (
                    "RUNNING"
                    if state["running"]
                    else "STOPPED"
                )

                print(
                    f"- {state['name']} ({status})"
                )

        print()

        print("Starting services...")

        results = self.start_services()

        self._print_results(
            results,
        )

        print()

        print(
            "Platform initialization complete."
        )

        return results