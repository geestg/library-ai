from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class LaunchSpec:

    name: str

    command: list[str]

    workdir: Path

    host: str

    port: int

    health_check: bool = True

    health_endpoint: str = "/health"

    environment: dict[str, str] | None = None