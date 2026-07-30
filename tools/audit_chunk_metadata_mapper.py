from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

print("=" * 70)
print("ChunkMetadataMapper Audit")
print("=" * 70)

mapper_file = (
    ROOT
    / "delbot_platform/documents/metadata/mapper/chunk_metadata_mapper.py"
)

if not mapper_file.exists():
    print("Mapper file not found")
    raise SystemExit

tree = ast.parse(
    mapper_file.read_text(
        encoding="utf-8",
    )
)

print()
print("FILE")
print(mapper_file.relative_to(ROOT))
print()

for node in tree.body:

    if isinstance(node, ast.ClassDef):
        if node.name != "ChunkMetadataMapper":
            continue

        print("CLASS :", node.name)
        print()

        for item in node.body:

            if isinstance(item, ast.FunctionDef):

                args = []

                for arg in item.args.args:
                    args.append(arg.arg)

                print(item.name)
                print("ARGS :", ", ".join(args))
                print()

print("=" * 70)
print("Searching from_payload callers")
print("=" * 70)

for py in ROOT.rglob("*.py"):

    if ".venv" in py.parts:
        continue

    if "__pycache__" in py.parts:
        continue

    try:
        source = py.read_text(
            encoding="utf-8",
        )
    except Exception:
        continue

    if "from_payload(" not in source:
        continue

    print()
    print(py.relative_to(ROOT))

    try:
        tree = ast.parse(source)
    except Exception:
        continue

    class Visitor(ast.NodeVisitor):

        def visit_Call(self, node):

            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "from_payload"
            ):

                print(
                    f"  line {node.lineno}"
                )

                print(
                    "  positional:",
                    len(node.args),
                )

                if node.keywords:

                    print(
                        "  keywords:"
                    )

                    for kw in node.keywords:

                        print(
                            "   -",
                            kw.arg,
                        )

            self.generic_visit(node)

    Visitor().visit(tree)

print()
print("=" * 70)
print("Searching default_chunk_id")
print("=" * 70)

for py in ROOT.rglob("*.py"):

    if ".venv" in py.parts:
        continue

    if "__pycache__" in py.parts:
        continue

    try:
        text = py.read_text(
            encoding="utf-8",
        )
    except Exception:
        continue

    if "default_chunk_id" in text:

        print(py.relative_to(ROOT))

print()
print("=" * 70)
print("DONE")
print("=" * 70)
