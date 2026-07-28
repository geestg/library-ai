from __future__ import annotations

import subprocess
import time
from pathlib import Path

import requests

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_monitor import (
    ProcessMonitor,
)
from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)


class ProcessManager:

    HEALTH_TIMEOUT = 30

    HEALTH_INTERVAL = 1.0

    def __init__(self):

        self.registry = ProcessRegistry()

        self.monitor = ProcessMonitor()

    def _wait_until_ready(
        self,
        process: subprocess.Popen,
        host: str,
        port: int,
    ) -> None:

        deadline = time.time() + self.HEALTH_TIMEOUT

        url = f"http://{host}:{port}/health"

        while time.time() < deadline:

            exit_code = process.poll()

            if exit_code is not None:

                raise RuntimeError(
                    f"Process exited during startup "
                    f"(exit_code={exit_code})"
                )

            try:

                response = requests.get(
                    url,
                    timeout=1,
                )

                if response.status_code == 200:

                    return

            except requests.RequestException:

                pass

            time.sleep(
                self.HEALTH_INTERVAL
            )

        raise TimeoutError(
            f"Health check timeout: {url}"
        )

    def start(
        self,
        *,
        name: str,
        command: list[str],
        workdir: Path,
        host="127.0.0.1",
        port=0,
    ):

        log_dir = workdir / "runtime"

        log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_file = open(
            log_dir / f"{name}.log",
            "ab",
        )

        process = subprocess.Popen(
            command,
            cwd=workdir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        self._wait_until_ready(
            process,
            host,
            port,
        )

        info = ProcessInfo(
            name=name,
            command=command,
            workdir=workdir,
            pid=process.pid,
            process=process,
            running=True,
            host=host,
            port=port,
        )

        self.registry.register(
            info
        )

        return info

    def stop(
        self,
        name: str,
    ):

        info = self.registry.get(
            name
        )

        if info is None:

            return False

        if info.process:

            info.process.terminate()

        info.running = False

        self.registry.register(
            info
        )

        return True

    def get(
        self,
        name: str,
    ):

        info = self.registry.get(
            name
        )

        if info:

            return self.monitor.refresh(
                info
            )

        return None

    def list(self):

        return [

            self.monitor.refresh(
                x
            )

            for x in self.registry.list()

        ]
