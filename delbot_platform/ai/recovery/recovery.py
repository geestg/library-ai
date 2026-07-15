import json
import os

from delbot_platform.core.runtime_manager import (
    RuntimeManager,
)


class RecoveryManager:

    @staticmethod
    def process_alive(
        pid: int,
    ) -> bool:

        try:

            os.kill(
                pid,
                0,
            )

            return True

        except OSError:

            return False

    @classmethod
    def load_states(cls):

        RuntimeManager.ensure_directories()

        states = []

        for file in RuntimeManager.STATE_DIR.glob("*.json"):

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                state = json.load(f)

            pid = state.get("pid")

            state["running"] = (

                pid is not None

                and

                cls.process_alive(pid)

            )

            states.append(state)

        return states