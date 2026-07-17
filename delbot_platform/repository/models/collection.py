from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Collection:

    id: str

    repository_id: str

    name: str

    path: str
