from __future__ import annotations

import time

from delbot_platform.boot.service_health import (
    ServiceHealth,
)


class ServiceWaiter:

    def __init__(
        self,
        timeout: int = 30,
        interval: float = 1.0,
    ):

        self.timeout = timeout
        self.interval = interval
        self.health = ServiceHealth()

    def wait(
        self,
        host: str,
        port: int,
        endpoint: str = "/health",
    ) -> bool:

        start = time.time()

        while True:

            if self.health.check(
                host=host,
                port=port,
                endpoint=endpoint,
            ):

                return True

            elapsed = (
                time.time()
                - start
            )

            if elapsed >= self.timeout:

                raise TimeoutError(
                    f"Service {host}:{port}{endpoint} "
                    f"did not become healthy within "
                    f"{self.timeout} seconds."
                )

            time.sleep(
                self.interval,
            )