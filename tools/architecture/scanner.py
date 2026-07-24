from __future__ import annotations

import ast
from pathlib import Path

from .resolver import (
    ImportResolver,
)


class PythonImportScanner:

    def __init__(
        self,
        project_root: Path,
    ) -> None:

        self.project_root = project_root
        self.resolver = ImportResolver()

    def scan(
        self,
        path: Path,
    ) -> list[str]:

        source = path.read_text(
            encoding="utf-8",
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

        imports: list[str] = []

        for node in ast.walk(tree):

            if not isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom,
                ),
            ):
                continue

            imports.extend(
                self.resolver.resolve(
                    file=path,
                    node=node,
                    project_root=self.project_root,
                )
            )

        return sorted(
            set(imports),
        )
