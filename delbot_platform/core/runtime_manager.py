from pathlib import Path

from delbot_platform.core.path_manager import PathManager


class RuntimeManager:
    """
    Runtime filesystem manager.

    Responsible for managing all runtime artifacts such as:

    runtime/
        pid/
        socket/
        state/
        tmp/
    """

    RUNTIME = PathManager.RUNTIME

    PID_DIR = RUNTIME / "pid"

    SOCKET_DIR = RUNTIME / "socket"

    STATE_DIR = RUNTIME / "state"

    TMP_DIR = RUNTIME / "tmp"

    @classmethod
    def ensure_directories(cls) -> None:

        for directory in (
            cls.PID_DIR,
            cls.SOCKET_DIR,
            cls.STATE_DIR,
            cls.TMP_DIR,
        ):

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    @classmethod
    def pid_file(
        cls,
        service: str,
    ) -> Path:

        return cls.PID_DIR / f"{service}.pid"

    @classmethod
    def socket_file(
        cls,
        service: str,
    ) -> Path:

        return cls.SOCKET_DIR / f"{service}.sock"

    @classmethod
    def state_file(
        cls,
        service: str,
    ) -> Path:

        return cls.STATE_DIR / f"{service}.json"