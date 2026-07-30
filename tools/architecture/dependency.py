from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .filter import RepositoryFilter
from .graph import DependencyGraphBuilder
from .inventory import RepositoryInventoryBuilder
from .models import (
    DependencyReport,
    ModuleDependency,
)
from .scanner import PythonImportScanner


class DependencyAnalyzer:

    def analyze(
        self,
        root: Path,
    ) -> DependencyReport:

        inventory = RepositoryInventoryBuilder().build(root)

        inventory = RepositoryFilter().filter_python_sources(
            inventory,
        )

        scanner = PythonImportScanner(
            project_root=root.parent,
        )

        report = DependencyReport()

        for entry in inventory.files:

            file = entry.path

            imports = scanner.scan(file)

            module = (
                file.relative_to(root.parent)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )

            report.modules.append(
                ModuleDependency(
                    module=module,
                    imports=sorted(set(imports)),
                )
            )

        return report


def write_json(
    report: DependencyReport,
    output: Path,
):

    graph = DependencyGraphBuilder().build(report)

    data = {
        "summary": {
            "modules": len(report.modules),
            "edges": len(graph.edges()),
            "imports": sum(
                len(m.imports)
                for m in report.modules
            ),
        },
        "modules": [
            asdict(module)
            for module in report.modules
        ],
    }

    output.write_text(
        json.dumps(
            data,
            indent=4,
        ),
        encoding="utf-8",
    )


def write_csv(
    report: DependencyReport,
    output: Path,
):

    with output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.writer(fp)

        writer.writerow(
            [
                "module",
                "import_count",
                "imports",
            ]
        )

        for module in sorted(
            report.modules,
            key=lambda m: m.module,
        ):

            writer.writerow(
                [
                    module.module,
                    len(module.imports),
                    ";".join(module.imports),
                ]
            )


def write_markdown(
    report: DependencyReport,
    output: Path,
):

    graph = DependencyGraphBuilder().build(report)

    total_modules = len(report.modules)

    total_edges = len(graph.edges())

    total_imports = sum(
        len(module.imports)
        for module in report.modules
    )

    average = (
        total_imports / total_modules
        if total_modules
        else 0
    )

    top_importers = sorted(
        report.modules,
        key=lambda m: len(m.imports),
        reverse=True,
    )[:20]

    lines = [
        "# DELBot Architecture Dependency",
        "",
        "## Summary",
        "",
        f"Modules : {total_modules}",
        f"Edges : {total_edges}",
        f"Imports : {total_imports}",
        f"Average Imports : {average:.2f}",
        "",
        "## Top Importers",
        "",
        "| Module | Imports |",
        "|---------|---------|",
    ]

    for module in top_importers:

        lines.append(
            f"| {module.module} | {len(module.imports)} |"
        )

    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():

    root = Path(__file__).resolve().parents[2]

    report = DependencyAnalyzer().analyze(root)

    reports = root / "reports"

    reports.mkdir(
        exist_ok=True,
    )

    write_json(
        report,
        reports / "architecture_dependency.json",
    )

    write_csv(
        report,
        reports / "architecture_dependency.csv",
    )

    write_markdown(
        report,
        reports / "architecture_dependency.md",
    )

    graph = DependencyGraphBuilder().build(report)

    print()

    print("Dependency graph generated")

    print(f"Modules : {len(report.modules)}")
    print(f"Edges   : {len(graph.edges())}")

    print()


if __name__ == "__main__":
    main()