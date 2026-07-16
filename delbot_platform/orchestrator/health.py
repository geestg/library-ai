from __future__ import annotations

from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)
from delbot_platform.boot.service_health import (
    ServiceHealth,
)


class HealthOrchestrator:

    def __init__(self) -> None:

        self.registry = ProcessRegistry()

        self.health = ServiceHealth()

    def services(self) -> list[dict]:

        return self.registry.load_runtime_states()

    def run(self) -> None:

        print()
        print("===================================")
        print("DELBot Platform Health")
        print("===================================")
        print()

        states = self.services()

        if not states:

            print("No services registered.")
            print()
            return

        for state in states:

            if not state["running"]:

                status = "STOPPED"

            else:

                ok = self.health.check(
                    host=state["host"],
                    port=state["port"],
                )

                status = (
                    "HEALTHY"
                    if ok
                    else "UNHEALTHY"
                )

            print(
                f"{state['name']:<15}{status}"
            )

        print()