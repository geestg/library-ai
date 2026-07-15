from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class ProcessInfo:

    name: str

    command: list[str]

    workdir: Path

    pid: Optional[int] = None

    process: object | None = None

    running: bool = False

    host: str = "127.0.0.1"

    port: int = 0

    def to_dict(self):

        return {

            "name": self.name,

            "command": self.command,

            "workdir": str(self.workdir),

            "pid": self.pid,

            "running": self.running,

            "host": self.host,

            "port": self.port,

        }