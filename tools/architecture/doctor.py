from __future__ import annotations

from pathlib import Path

from tools.architecture.models import (
    ArchitectureReport,
)
from tools.architecture.pipeline import (
    ArchitecturePipeline,
)


class ArchitectureDoctor:

    def analyze(
        self,
        root: Path,
        module_layers: dict[str, str] | None = None,
        allowed_dependencies: dict[str, set[str]] | None = None,
    ) -> ArchitectureReport:

        return ArchitecturePipeline().analyze(
            root=root,
            module_layers=module_layers,
            allowed_dependencies=allowed_dependencies,
        )
