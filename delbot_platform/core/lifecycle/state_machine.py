"""
DELBot Lifecycle State Machine.

Defines valid lifecycle transitions for managed services.
"""

from __future__ import annotations

from .service_state import ServiceState


_ALLOWED_TRANSITIONS: dict[ServiceState, frozenset[ServiceState]] = {
    ServiceState.STOPPED: frozenset({
        ServiceState.INITIALIZING,
    }),

    ServiceState.INITIALIZING: frozenset({
        ServiceState.STARTING,
        ServiceState.FAILED,
    }),

    ServiceState.STARTING: frozenset({
        ServiceState.WARMING_UP,
        ServiceState.FAILED,
    }),

    ServiceState.WARMING_UP: frozenset({
        ServiceState.READY,
        ServiceState.FAILED,
    }),

    ServiceState.READY: frozenset({
        ServiceState.RUNNING,
        ServiceState.STOPPING,
    }),

    ServiceState.RUNNING: frozenset({
        ServiceState.DEGRADED,
        ServiceState.STOPPING,
        ServiceState.FAILED,
    }),

    ServiceState.DEGRADED: frozenset({
        ServiceState.RUNNING,
        ServiceState.RECOVERING,
        ServiceState.STOPPING,
    }),

    ServiceState.RECOVERING: frozenset({
        ServiceState.RUNNING,
        ServiceState.FAILED,
    }),

    ServiceState.FAILED: frozenset({
        ServiceState.RECOVERING,
        ServiceState.STOPPED,
    }),

    ServiceState.STOPPING: frozenset({
        ServiceState.STOPPED,
    }),
}


class StateMachine:
    """Lifecycle transition validator."""

    @staticmethod
    def can_transition(
        current: ServiceState,
        target: ServiceState,
    ) -> bool:
        return target in _ALLOWED_TRANSITIONS.get(current, frozenset())
