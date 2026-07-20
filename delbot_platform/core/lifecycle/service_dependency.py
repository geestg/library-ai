"""
DELBot Service Dependency Model.

Defines dependency relationships between managed services.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ServiceDependency:
    """
    Dependency definition for a managed service.
    """

    service: str

    requires: tuple[str, ...] = field(default_factory=tuple)

    optional: tuple[str, ...] = field(default_factory=tuple)

    startup_priority: int = 100

    shutdown_priority: int = 100

    health_required: bool = True
