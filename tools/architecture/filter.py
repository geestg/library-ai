from __future__ import annotations

from .models import (
    RepositoryFile,
    RepositoryInventory,
)


class RepositoryFilter:

    EXCLUDED_CATEGORIES = {
        "backup",
        "pycache",
        "stage",
        "step",
    }

    def filter_python_sources(
        self,
        inventory: RepositoryInventory,
    ) -> RepositoryInventory:

        result = RepositoryInventory(
            root=inventory.root,
        )

        result.directories.extend(
            inventory.directories,
        )

        for file in inventory.files:

            if not self._is_python_source(
                file,
            ):
                continue

            result.files.append(
                file,
            )

        return result

    def _is_python_source(
        self,
        file: RepositoryFile,
    ) -> bool:

        if file.category in self.EXCLUDED_CATEGORIES:
            return False

        if file.extension != ".py":
            return False

        return True
