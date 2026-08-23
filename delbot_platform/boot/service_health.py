from __future__ import annotations

import httpx


class ServiceHealth:

    def __init__(
        self,
        timeout: float = 3.0,
    ):

        self.timeout = timeout

    def check(
        self,
        host: str,
        port: int,
        endpoint: str = "/health",
    ) -> bool:

        url = (
            f"http://{host}:{port}{endpoint}"
        )

        try:

            response = httpx.get(
                url,
                timeout=self.timeout,
            )

            return response.status_code == 200

        except Exception:

            return False