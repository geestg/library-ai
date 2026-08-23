from __future__ import annotations

from tools.architecture.graph import DependencyGraph


class DependencyGraphFilter:

    def internal(
        self,
        graph: DependencyGraph,
    ) -> DependencyGraph:

        modules = dict(graph.modules)

        outgoing: dict[str, set[str]] = {}
        incoming: dict[str, set[str]] = {}

        internal = set(modules.keys())

        for source, targets in graph.outgoing.items():

            if source not in internal:
                continue

            outgoing[source] = {
                target
                for target in targets
                if target in internal
            }

        for target, sources in graph.incoming.items():

            if target not in internal:
                continue

            incoming[target] = {
                source
                for source in sources
                if source in internal
            }

        return DependencyGraph(
            modules=modules,
            outgoing=outgoing,
            incoming=incoming,
        )
