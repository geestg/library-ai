from __future__ import annotations

from tools.architecture.graph import DependencyGraph
from tools.architecture.models import (
    CircularDependency,
    CircularDependencyReport,
)


class CircularAnalyzer:

    def __init__(self) -> None:

        self._graph: DependencyGraph | None = None

        self._index = 0

        self._stack: list[str] = []

        self._on_stack: set[str] = set()

        self._indices: dict[str, int] = {}

        self._lowlinks: dict[str, int] = {}

        self._cycles: list[CircularDependency] = []

    def analyze(
        self,
        graph: DependencyGraph,
    ) -> CircularDependencyReport:

        self._graph = graph

        self._initialize()

        for module in sorted(
            graph.nodes(),
        ):

            if module not in self._indices:

                self._strong_connect(
                    module,
                )

        self._cycles.sort(
            key=lambda cycle: cycle.modules,
        )

        return CircularDependencyReport(
            cycles=list(self._cycles),
        )

    def _initialize(
        self,
    ) -> None:

        self._index = 0

        self._stack.clear()

        self._on_stack.clear()

        self._indices.clear()

        self._lowlinks.clear()

        self._cycles.clear()

    def _strong_connect(
        self,
        module: str,
    ) -> None:

        self._indices[module] = self._index
        self._lowlinks[module] = self._index

        self._index += 1

        self._stack.append(
            module,
        )

        self._on_stack.add(
            module,
        )

        assert self._graph is not None

        for dependency in sorted(
            self._graph.dependencies(
                module,
            )
        ):

            if dependency not in self._indices:

                self._strong_connect(
                    dependency,
                )

                self._lowlinks[module] = min(
                    self._lowlinks[module],
                    self._lowlinks[dependency],
                )

            elif dependency in self._on_stack:

                self._lowlinks[module] = min(
                    self._lowlinks[module],
                    self._indices[dependency],
                )

        if self._lowlinks[module] != self._indices[module]:
            return

        component: list[str] = []

        while True:

            node = self._stack.pop()

            self._on_stack.remove(
                node,
            )

            component.append(
                node,
            )

            if node == module:
                break

        if len(component) <= 1:
            return

        self._cycles.append(
            CircularDependency(
                modules=tuple(
                    sorted(component),
                ),
            )
        )
