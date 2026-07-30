from __future__ import annotations

import ast
import csv
import json
from dataclasses import asdict
from pathlib import Path

from .filter import RepositoryFilter
from .models import (
    RepositoryFile,
    RepositoryInventory,
)


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "reports",
    "runtime",
    "qdrant_storage",
}


class RepositoryInventoryBuilder:

    def build(
        self,
        root: Path,
    ) -> RepositoryInventory:

        inventory = RepositoryInventory(
            root=root,
        )

        for directory in sorted(
            p
            for p in root.rglob("*")
            if p.is_dir()
        ):

            if self._excluded(directory):
                continue

            inventory.directories.append(
                directory.relative_to(root),
            )

        for file in sorted(
            p
            for p in root.rglob("*")
            if p.is_file()
        ):

            if self._excluded(file):
                continue

            inventory.files.append(
                RepositoryFile(
                    path=file,
                    relative_path=file.relative_to(root),
                    extension=file.suffix,
                    category=self._categorize(file),
                )
            )

        return inventory

    def _excluded(
        self,
        path: Path,
    ) -> bool:

        return any(
            part in EXCLUDED_DIRS
            for part in path.parts
        )

    def _categorize(
        self,
        path: Path,
    ) -> str:

        name = path.name

        if "__pycache__" in path.parts:
            return "pycache"

        if name == "__init__.py":
            return "init"

        if path.suffix == ".py":
            return "python"

        if path.suffix == ".md":
            return "markdown"

        if path.suffix == ".json":
            return "json"

        if path.suffix == ".yaml":
            return "yaml"

        if path.suffix == ".yml":
            return "yaml"

        if path.suffix == ".txt":
            return "text"

        return "other"


class SymbolScanner:

    def scan(
        self,
        path: Path,
    ) -> dict:

        result = {
            "classes": [],
            "functions": [],
            "async_functions": [],
            "dataclasses": [],
            "enums": [],
        }

        if path.suffix != ".py":
            return result

        try:

            source = path.read_text(
                encoding="utf-8",
            )

            tree = ast.parse(source)

        except Exception:

            return result

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                result["classes"].append(
                    node.name,
                )

                decorators = {
                    getattr(d, "id", "")
                    for d in node.decorator_list
                }

                if "dataclass" in decorators:
                    result["dataclasses"].append(
                        node.name,
                    )

                for base in node.bases:

                    if getattr(base, "id", "") == "Enum":
                        result["enums"].append(
                            node.name,
                        )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                result["functions"].append(
                    node.name,
                )

            elif isinstance(
                node,
                ast.AsyncFunctionDef,
            ):

                result["async_functions"].append(
                    node.name,
                )

        return result


def write_json(
    inventory: RepositoryInventory,
    report: Path,
):

    scanner = SymbolScanner()

    data = []

    for f in inventory.files:

        symbols = scanner.scan(
            f.path,
        )

        item = asdict(f)

        item["path"] = str(f.path)
        item["relative_path"] = str(f.relative_path)

        item.update(symbols)

        item["size"] = f.path.stat().st_size

        item["lines"] = sum(
            1
            for _
            in f.path.open(
                encoding="utf-8",
                errors="ignore",
            )
        )

        data.append(item)

    report.write_text(
        json.dumps(
            data,
            indent=4,
        ),
        encoding="utf-8",
    )


def write_csv(
    inventory: RepositoryInventory,
    report: Path,
):

    scanner = SymbolScanner()

    with report.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.writer(fp)

        writer.writerow(
            [
                "path",
                "category",
                "extension",
                "lines",
                "size",
                "classes",
                "functions",
                "async_functions",
            ]
        )

        for f in inventory.files:

            s = scanner.scan(
                f.path,
            )

            writer.writerow(
                [
                    str(f.relative_path),
                    f.category,
                    f.extension,
                    sum(
                        1
                        for _
                        in f.path.open(
                            encoding="utf-8",
                            errors="ignore",
                        )
                    ),
                    f.path.stat().st_size,
                    len(s["classes"]),
                    len(s["functions"]),
                    len(s["async_functions"]),
                ]
            )


def write_markdown(
    inventory: RepositoryInventory,
    report: Path,
):

    total_py = sum(
        1
        for f in inventory.files
        if f.extension == ".py"
    )

    total_lines = 0

    for f in inventory.files:

        try:

            total_lines += sum(
                1
                for _
                in f.path.open(
                    encoding="utf-8",
                    errors="ignore",
                )
            )

        except Exception:

            pass

    text = f"""# DELBot Architecture Inventory

## Summary

Directories : {len(inventory.directories)}

Files : {len(inventory.files)}

Python Files : {total_py}

Total Lines : {total_lines}
"""

    report.write_text(
        text,
        encoding="utf-8",
    )


def main():

    root = Path(__file__).resolve().parents[2]

    inventory = RepositoryInventoryBuilder().build(
        root,
    )

    inventory = RepositoryFilter().filter_python_sources(
        inventory,
    )

    reports = root / "reports"

    reports.mkdir(
        exist_ok=True,
    )

    write_json(
        inventory,
        reports / "architecture_inventory.json",
    )

    write_csv(
        inventory,
        reports / "architecture_inventory.csv",
    )

    write_markdown(
        inventory,
        reports / "architecture_inventory.md",
    )

    print()

    print("Inventory generated")

    print(f"Python files : {len(inventory.files)}")

    print()


if __name__ == "__main__":
    main()