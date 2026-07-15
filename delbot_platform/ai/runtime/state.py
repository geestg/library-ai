from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RuntimeState:

    name: str

    command: list[str]

    workdir: Path

    host: str

    port: int

    pid: int | None = None

    running: bool = False