from __future__ import annotations

import ast
from pathlib import Path


class ImportResolver:

    def resolve(
        self,
        *,
        file: Path,
        node: ast.AST,
        project_root: Path,
    ) -> list[str]:

        if isinstance(node, ast.Import):
            return sorted(
                {
                    alias.name
                    for alias in node.names
                }
            )

        if not isinstance(
            node,
            ast.ImportFrom,
        ):
            return []

        base = self._resolve_base(
            file=file,
            level=node.level,
            module=node.module or "",
            project_root=project_root,
        )

        if not base:
            return []

        return [base]

    def _resolve_base(
        self,
        *,
        file: Path,
        level: int,
        module: str,
        project_root: Path,
    ) -> str:

        #
        # Absolute import
        #
        # from pathlib import Path
        # from dataclasses import dataclass
        # from delbot_platform.ai.embedding import embedding_request
        #
        if level == 0:
            return module

        current = (
            file.relative_to(project_root)
            .with_suffix("")
            .parts
        )

        package = list(current[:-1])

        #
        # Relative import
        #
        # level=1 -> from .models import X
        # level=2 -> from ..core import Y
        #
        keep = max(
            0,
            len(package) - (level - 1),
        )

        package = package[:keep]

        if module:
            package.extend(
                module.split(".")
            )

        return ".".join(package)
