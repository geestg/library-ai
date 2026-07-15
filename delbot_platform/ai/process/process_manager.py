from __future__ import annotations

import subprocess
from pathlib import Path

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)


class ProcessManager:

    def __init__(self) -> None:

        self.registry = ProcessRegistry()

    #
    # Lifecycle
    #

    def start(
        self,
        *,
        name: str,
        command: list[str],
        workdir: Path,
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> ProcessInfo:

        proc = subprocess.Popen(
            command,
            cwd=workdir,
        )

        info = ProcessInfo(
            name=name,
            command=command,
            workdir=workdir,
            pid=proc.pid,
            process=proc,
            running=True,
            host=host,
            port=port,
        )

        self.registry.register(
            info,
        )

        return info

    def stop(
        self,
        name: str,
    ) -> bool:

        process = self.registry.get(
            name,
        )

        if process is None:

            return False

        if process.process is not None:

            process.process.terminate()

            process.process.wait()

        process.process = None
        process.running = False
        process.pid = None

        self.registry.register(
            process,
        )

        return True

    #
    # Query API
    #

    def get(
        self,
        name: str,
    ) -> ProcessInfo | None:

        return self.registry.get(
            name,
        )

    def list(
        self,
    ) -> list[ProcessInfo]:

        return self.registry.list()

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.registry.exists(
            name,
        )

    def running(
        self,
        name: str,
    ) -> bool:

        process = self.registry.get(
            name,
        )

        if process is None:

            return False

        return process.running