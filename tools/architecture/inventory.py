from __future__ import annotations

from pathlib import Path

from .models import (
    RepositoryFile,
    RepositoryInventory,
)


class RepositoryInventoryBuilder:

    def build(
        self,
        root: Path,
    ) -> RepositoryInventory:

        inventory = RepositoryInventory(
            root=root,
        )

        inventory.directories.extend(
            sorted(
                p.relative_to(root)
                for p in root.rglob("*")
                if p.is_dir()
            )
        )

        for file in sorted(
            p
            for p in root.rglob("*")
            if p.is_file()
        ):

            inventory.files.append(
                RepositoryFile(
                    path=file,
                    relative_path=file.relative_to(root),
                    extension=file.suffix,
                    category=self._categorize(file),
                )
            )

        return inventory

    def _categorize(
        self,
        path: Path,
    ) -> str:

        name = path.name

        if "__pycache__" in path.parts:
            return "pycache"

        if name.endswith(".stage"):
            return "stage"

        if ".stage" in name:
            return "stage"

        if name.endswith(".bak"):
            return "backup"

        if name.endswith(".backup"):
            return "backup"

        if ".before_" in name:
            return "backup"

        if ".step" in name:
            return "step"

        if name == "__init__.py":
            return "init"

        if path.suffix == ".py":
            return "python"

        return "other"
