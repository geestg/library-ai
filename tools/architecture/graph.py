from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from tools.architecture.models import DependencyReport
from tools.architecture.models import ModuleDependency


@dataclass(slots=True)
class DependencyGraph:

    modules: dict[str, ModuleDependency]

    outgoing: dict[str, set[str]]

    incoming: dict[str, set[str]]

    def has(
        self,
        module: str,
    ) -> bool:

        return module in self.modules

    def nodes(
        self,
    ) -> set[str]:

        return set(self.modules)

    def edges(
        self,
    ) -> set[tuple[str, str]]:

        edges: set[tuple[str, str]] = set()

        for source, targets in self.outgoing.items():

            for target in targets:
                edges.add(
                    (
                        source,
                        target,
                    )
                )

        return edges

    def dependencies(
        self,
        module: str,
    ) -> set[str]:

        return set(
            self.outgoing.get(
                module,
                set(),
            )
        )

    def dependents(
        self,
        module: str,
    ) -> set[str]:

        return set(
            self.incoming.get(
                module,
                set(),
            )
        )

    def neighbors(
        self,
        module: str,
    ) -> set[str]:

        return (
            self.dependencies(module)
            |
            self.dependents(module)
        )

    def out_degree(
        self,
        module: str,
    ) -> int:

        return len(
            self.outgoing.get(
                module,
                set(),
            )
        )

    def in_degree(
        self,
        module: str,
    ) -> int:

        return len(
            self.incoming.get(
                module,
                set(),
            )
        )

    def is_root(
        self,
        module: str,
    ) -> bool:

        return self.in_degree(module) == 0

    def is_leaf(
        self,
        module: str,
    ) -> bool:

        return self.out_degree(module) == 0


@dataclass(slots=True)
class DependencyGraphBuilder:

    _modules: dict[str, ModuleDependency] = field(
        default_factory=dict,
    )

    _outgoing: dict[str, set[str]] = field(
        default_factory=dict,
    )

    _incoming: dict[str, set[str]] = field(
        default_factory=dict,
    )

    def build(
        self,
        report: DependencyReport,
    ) -> DependencyGraph:

        self._modules.clear()
        self._outgoing.clear()
        self._incoming.clear()

        #
        # Register modules
        #
        for module in report.modules:

            self._modules[module.module] = module

            self._outgoing.setdefault(
                module.module,
                set(),
            )

            self._incoming.setdefault(
                module.module,
                set(),
            )

        #
        # Register edges
        #
        for module in report.modules:

            source = module.module

            for target in module.imports:

                if source == target:
                    continue

                self._outgoing.setdefault(
                    source,
                    set(),
                ).add(target)

                self._incoming.setdefault(
                    target,
                    set(),
                ).add(source)

        return DependencyGraph(
            modules=dict(self._modules),
            outgoing={
                key: set(value)
                for key, value in self._outgoing.items()
            },
            incoming={
                key: set(value)
                for key, value in self._incoming.items()
            },
        )
