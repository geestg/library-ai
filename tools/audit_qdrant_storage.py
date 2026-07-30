from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "delbot_platform/vectorstore/qdrant/client.py",
    "delbot_platform/vectorstore/qdrant/repository.py",
    "delbot_platform/vectorstore/qdrant/singleton.py",
    "delbot_platform/vectorstore/__init__.py",
    "delbot_platform/vectors/vector_record.py",
]

KEYWORDS = [
    "collection_name",
    "collection",
    "host",
    "port",
    "url",
    "QdrantClient",
    "upsert",
    "scroll",
    "search",
    "count",
    "payload",
    "document_id",
    "PointStruct",
    "except",
    "try",
]

print("=" * 70)
print("QDRANT STORAGE AUDIT")
print("=" * 70)

for rel in FILES:

    file = ROOT / rel

    print()
    print("-" * 70)
    print(rel)
    print("-" * 70)

    if not file.exists():
        print("FILE NOT FOUND")
        continue

    source = file.read_text(
        encoding="utf-8",
    )

    tree = ast.parse(source)

    print("\nCLASSES")
    print("-------")

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            print(node.name)

    print("\nFUNCTIONS")
    print("---------")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print(node.name)

    print("\nKEYWORDS")
    print("--------")

    for word in KEYWORDS:
        if word in source:
            print(word)

    print("\nCLIENT CALLS")
    print("------------")

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            func = node.func

            if isinstance(func, ast.Attribute):

                name = func.attr

                if name in {
                    "upsert",
                    "scroll",
                    "search",
                    "count",
                    "create_collection",
                    "collection_exists",
                }:

                    print(name)

    print("\nTRY/EXCEPT")
    print("----------")

    found = False

    for node in ast.walk(tree):

        if isinstance(node, ast.Try):

            found = True

            print(
                "try at line",
                node.lineno,
            )

            if not node.handlers:
                continue

            for handler in node.handlers:

                if handler.type is None:
                    print(
                        "  except: (bare)"
                    )

                elif isinstance(
                    handler.type,
                    ast.Name,
                ):
                    print(
                        "  except",
                        handler.type.id,
                    )

                else:
                    print(
                        "  except <complex>"
                    )

    if not found:
        print("NONE")

print()
print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
