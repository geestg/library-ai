from __future__ import annotations

from pathlib import Path

from .filter import RepositoryFilter
from .inventory import RepositoryInventoryBuilder
from .models import DependencyReport
from .models import ModuleDependency
from .scanner import PythonImportScanner


class DependencyAnalyzer:

    def analyze(
        self,
        root: Path,
    ) -> DependencyReport:

        inventory = RepositoryInventoryBuilder().build(
            root,
        )

        inventory = RepositoryFilter().filter_python_sources(
            inventory,
        )

        scanner = PythonImportScanner(
            project_root=root.parent,
        )

        report = DependencyReport()

        for entry in inventory.files:

            file = entry.path

            imports = scanner.scan(
                file,
            )

            module = (
                file.relative_to(root.parent)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )

            report.modules.append(
                ModuleDependency(
                    module=module,
                    imports=imports,
                )
            )

        return report
