"""
DELBot Boot Policy.

Defines how a platform service should be started and recovered.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StartupMode(str, Enum):
    """Service startup strategy."""

    ALWAYS = "always"
    LAZY = "lazy"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class BootPolicy:
    """
    Immutable boot policy for a managed service.
    """

    startup: StartupMode = StartupMode.ALWAYS

    auto_restart: bool = True

    max_restart: int = 3

    startup_timeout: int = 300

    health_timeout: int = 60

    dependency_required: bool = True
