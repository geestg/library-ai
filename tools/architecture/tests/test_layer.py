from __future__ import annotations

from tools.architecture.graph import DependencyGraph
from tools.architecture.layer import LayerAnalyzer
from tools.architecture.models import (
    LayerViolation,
    ModuleDependency,
)


def build_graph(
    edges: dict[str, set[str]],
) -> DependencyGraph:

    modules = {
        module: ModuleDependency(
            module=module,
        )
        for module in edges
    }

    outgoing = {
        module: set(targets)
        for module, targets in edges.items()
    }

    incoming = {
        module: set()
        for module in edges
    }

    for source, targets in outgoing.items():

        for target in targets:

            incoming.setdefault(
                target,
                set(),
            ).add(source)

    return DependencyGraph(
        modules=modules,
        outgoing=outgoing,
        incoming=incoming,
    )


def analyze(
    graph: DependencyGraph,
    layers: dict[str, str],
    rules: dict[str, set[str]],
) -> list[LayerViolation]:

    report = LayerAnalyzer().analyze(
        graph=graph,
        module_layers=layers,
        allowed_dependencies=rules,
    )

    return report.violations


def test_valid_dependency() -> None:

    graph = build_graph(
        {
            "api": {"service"},
            "service": set(),
        }
    )

    violations = analyze(
        graph,
        {
            "api": "api",
            "service": "application",
        },
        {
            "api": {"application"},
            "application": set(),
        },
    )

    assert violations == []


def test_single_violation() -> None:

    graph = build_graph(
        {
            "domain": {"api"},
            "api": set(),
        }
    )

    violations = analyze(
        graph,
        {
            "domain": "domain",
            "api": "api",
        },
        {
            "domain": set(),
            "api": {"application"},
        },
    )

    assert len(violations) == 1


def test_multiple_violations() -> None:

    graph = build_graph(
        {
            "domain": {"api", "infra"},
            "api": set(),
            "infra": set(),
        }
    )

    violations = analyze(
        graph,
        {
            "domain": "domain",
            "api": "api",
            "infra": "infrastructure",
        },
        {
            "domain": set(),
        },
    )

    assert len(violations) == 2


def test_missing_layer_mapping() -> None:

    graph = build_graph(
        {
            "a": {"b"},
            "b": set(),
        }
    )

    violations = analyze(
        graph,
        {},
        {},
    )

    assert violations == []


def test_unknown_rule() -> None:

    graph = build_graph(
        {
            "a": {"b"},
            "b": set(),
        }
    )

    violations = analyze(
        graph,
        {
            "a": "layer1",
            "b": "layer2",
        },
        {},
    )

    assert len(violations) == 1
