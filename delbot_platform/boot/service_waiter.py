from __future__ import annotations

import socket
import time

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)


class ServiceWaiter:

    def __init__(
        self,
        timeout: int = 60,
        interval: float = 1.0,
    ) -> None:

        self.timeout = timeout
        self.interval = interval


    def wait(
        self,
        process: ProcessInfo,
    ) -> ProcessInfo:

        if process.port == 0:

            return process


        start = time.time()


        while True:

            if self._check_port(
                process.host,
                process.port,
            ):

                return process


            if time.time() - start > self.timeout:

                raise TimeoutError(
                    f"Service {process.name} "
                    f"failed waiting on "
                    f"{process.host}:{process.port}"
                )


            if process.process:

                exit_code = process.process.poll()

                if exit_code is not None:

                    raise RuntimeError(
                        f"Service {process.name} exited "
                        f"with code {exit_code}"
                    )


            time.sleep(
                self.interval
            )


    def _check_port(
        self,
        host: str,
        port: int,
    ) -> bool:

        try:

            with socket.create_connection(
                (host, port),
                timeout=1,
            ):
                return True

        except OSError:

            return False
