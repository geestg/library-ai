"""
DELBot Platform Lifecycle

Unified lifecycle state definition for every managed service.

This module is intentionally independent from Runtime, AI, Gateway,
and ProcessManager so it can be shared across the entire platform.
"""

from __future__ import annotations

from enum import Enum
from typing import Final


class ServiceState(str, Enum):
    """
    Canonical lifecycle state for every DELBot service.
    """

    STOPPED = "stopped"

    INITIALIZING = "initializing"

    STARTING = "starting"

    WARMING_UP = "warming_up"

    READY = "ready"

    RUNNING = "running"

    DEGRADED = "degraded"

    FAILED = "failed"

    RECOVERING = "recovering"

    STOPPING = "stopping"

    @property
    def is_active(self) -> bool:
        return self in ACTIVE_STATES

    @property
    def is_running(self) -> bool:
        return self in RUNNING_STATES

    @property
    def is_failure(self) -> bool:
        return self in FAILURE_STATES

    @property
    def is_terminal(self) -> bool:
        return self in TERMINAL_STATES

    @property
    def can_start(self) -> bool:
        return self in STARTABLE_STATES

    @property
    def can_stop(self) -> bool:
        return self in STOPPABLE_STATES

    @property
    def can_restart(self) -> bool:
        return self in RESTARTABLE_STATES


ACTIVE_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.INITIALIZING,
        ServiceState.STARTING,
        ServiceState.WARMING_UP,
        ServiceState.READY,
        ServiceState.RUNNING,
        ServiceState.DEGRADED,
        ServiceState.RECOVERING,
    }
)

RUNNING_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.READY,
        ServiceState.RUNNING,
        ServiceState.DEGRADED,
    }
)

FAILURE_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.FAILED,
    }
)

TERMINAL_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.STOPPED,
        ServiceState.FAILED,
    }
)

STARTABLE_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.STOPPED,
        ServiceState.FAILED,
    }
)

STOPPABLE_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.INITIALIZING,
        ServiceState.STARTING,
        ServiceState.WARMING_UP,
        ServiceState.READY,
        ServiceState.RUNNING,
        ServiceState.DEGRADED,
        ServiceState.RECOVERING,
    }
)

RESTARTABLE_STATES: Final[frozenset[ServiceState]] = frozenset(
    {
        ServiceState.RUNNING,
        ServiceState.DEGRADED,
        ServiceState.FAILED,
    }
)
