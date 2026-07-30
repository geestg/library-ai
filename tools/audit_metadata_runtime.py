from __future__ import annotations

import ast
import importlib
import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 70)
print("DOCUMENT METADATA AUDIT")
print("=" * 70)

print()
print("=" * 70)
print("1. SEARCH ChunkMetadata")
print("=" * 70)

matches = []

for file in ROOT.rglob("*.py"):

    if ".venv" in file.parts:
        continue

    try:
        tree = ast.parse(file.read_text(encoding="utf-8"))
    except Exception:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):
            if node.name == "ChunkMetadata":
                matches.append(file)

for file in matches:
    print(file.relative_to(ROOT))

print()
print("=" * 70)
print("2. SEARCH IMPORTS")
print("=" * 70)

imports = []

for file in ROOT.rglob("*.py"):

    if ".venv" in file.parts:
        continue

    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        continue

    if "ChunkMetadata" in text:
        imports.append(file)

for file in imports:
    print(file.relative_to(ROOT))

print()
print("=" * 70)
print("3. IMPORT TEST")
print("=" * 70)

CANDIDATES = [

    "delbot_platform.documents.metadata",

    "delbot_platform.documents.metadata.models",

    "delbot_platform.documents.metadata.model",

    "delbot_platform.documents.metadata.chunk_metadata",

    "delbot_platform.documents.metadata.models.chunk_metadata",

    "delbot_platform.documents.models.chunk_metadata",

]

for module in CANDIDATES:

    try:

        m = importlib.import_module(module)

        print(f"[PASS] {module}")

        for name in dir(m):
            if "ChunkMetadata" in name:
                print("   ", name)

    except Exception as exc:

        print(f"[FAIL] {module}")
        print(type(exc).__name__)
        print(exc)

print()
print("=" * 70)
print("4. LOCATE FILE")
print("=" * 70)

for file in ROOT.rglob("*chunk_metadata*.py"):

    if ".venv" in file.parts:
        continue

    print(file.relative_to(ROOT))

print()
print("=" * 70)
print("5. SHOW DATACLASS")
print("=" * 70)

for file in ROOT.rglob("*chunk_metadata*.py"):

    if ".venv" in file.parts:
        continue

    print()
    print(file.relative_to(ROOT))
    print("-" * 70)

    try:
        print(file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(exc)

print()
print("=" * 70)
print("DONE")
print("=" * 70)
