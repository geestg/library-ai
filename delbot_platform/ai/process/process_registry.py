from __future__ import annotations

import json

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)

from delbot_platform.core.runtime_manager import (
    RuntimeManager,
)


class ProcessRegistry:

    def __init__(self) -> None:

        self._processes: dict[str, ProcessInfo] = {}

    def register(
        self,
        process: ProcessInfo,
    ) -> None:
        """
        Register or update a process.
        """

        self._processes[process.name] = process

        self._save(process)

    def get(
        self,
        name: str,
    ) -> ProcessInfo | None:

        return self._processes.get(name)

    def list(
        self,
    ) -> list[ProcessInfo]:

        return list(
            self._processes.values()
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._processes

    def unregister(
        self,
        name: str,
    ) -> bool:

        process = self._processes.pop(
            name,
            None,
        )

        if process is None:

            return False

        self._remove(name)

        return True

    def clear(
        self,
    ) -> None:

        for name in list(
            self._processes.keys()
        ):

            self.unregister(name)

    def load_runtime_states(
        self,
    ) -> list[dict]:

        RuntimeManager.ensure_directories()

        states: list[dict] = []

        for file in RuntimeManager.STATE_DIR.glob(
            "*.json"
        ):

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                states.append(
                    json.load(f)
                )

        return states

    def _save(
        self,
        process: ProcessInfo,
    ) -> None:

        RuntimeManager.ensure_directories()

        state_file = RuntimeManager.state_file(
            process.name,
        )

        with open(
            state_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                process.to_dict(),
                f,
                indent=4,
            )

        pid_file = RuntimeManager.pid_file(
            process.name,
        )

        pid_file.write_text(
            str(process.pid),
            encoding="utf-8",
        )

    def _remove(
        self,
        name: str,
    ) -> None:

        state_file = RuntimeManager.state_file(
            name,
        )

        if state_file.exists():

            state_file.unlink()

        pid_file = RuntimeManager.pid_file(
            name,
        )

        if pid_file.exists():

            pid_file.unlink()