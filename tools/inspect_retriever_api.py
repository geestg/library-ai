from __future__ import annotations

import ast
import inspect
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 70)
print("RETRIEVER API")
print("=" * 70)

module = importlib.import_module(
    "delbot_platform.knowledge.retrieval.qdrant"
)

Retriever = getattr(module, "QdrantRetriever")

print()
print("CLASS")
print(Retriever)

print()
print("SIGNATURE")
print(inspect.signature(Retriever.retrieve))

print()
print("SOURCE")
print(inspect.getsource(Retriever.retrieve))

print()
print("=" * 70)
print("SEARCH CALLERS")
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

    if ".retrieve(" not in source:
        continue

    try:
        tree = ast.parse(source)
    except Exception:
        continue

    class Visitor(ast.NodeVisitor):

        def visit_Call(self, node):

            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "retrieve"
            ):

                print()
                print(py.relative_to(ROOT))
                print("line :", node.lineno)

                print("positional :", len(node.args))

                if node.keywords:

                    print("keywords")

                    for kw in node.keywords:

                        print(
                            "   ",
                            kw.arg,
                        )

            self.generic_visit(node)

    Visitor().visit(tree)

print()
print("=" * 70)
print("SEARCH EMBEDDING KEYWORD")
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

    if "embedding=" in text:

        print(py.relative_to(ROOT))

print()
print("=" * 70)
print("SEARCH RAG RETRIEVER")
print("=" * 70)

for py in ROOT.rglob("*.py"):

    if ".venv" in py.parts:
        continue

    if "__pycache__" in py.parts:
        continue

    try:
        tree = ast.parse(
            py.read_text(
                encoding="utf-8",
            )
        )
    except Exception:
        continue

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            for item in node.body:

                if (
                    isinstance(item, ast.FunctionDef)
                    and item.name in (
                        "search",
                        "retrieve",
                    )
                ):

                    print()
                    print(py.relative_to(ROOT))
                    print("CLASS :", node.name)
                    print("METHOD:", item.name)

print()
print("=" * 70)
print("DONE")
print("=" * 70)
