from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Repository:

    id: str

    name: str

    url: str

    type: str
