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
print("LOCATE CITATION MODEL")
print("=" * 70)

knowledge = ROOT / "delbot_platform" / "knowledge"

hits = []

for py in sorted(knowledge.rglob("*.py")):

    rel = py.relative_to(ROOT)

    try:
        tree = ast.parse(py.read_text(encoding="utf-8"))
    except Exception:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            if "citation" in node.name.lower():

                hits.append((str(rel), node.name))

print()

if not hits:
    print("NO CITATION CLASS FOUND")
else:
    for file, cls in hits:
        print(file)
        print("CLASS :", cls)
        print()

print("=" * 70)
print("SEARCH IMPORTS")
print("=" * 70)

for py in sorted(knowledge.rglob("*.py")):

    rel = py.relative_to(ROOT)

    text = py.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if "knowledge.models.citation" in text \
       or "Citation(" in text \
       or "from .citation" in text \
       or "import Citation" in text:

        print(rel)

print()
print("=" * 70)
print("IMPORT KNOWLEDGE PACKAGE")
print("=" * 70)

modules = [
    "delbot_platform.knowledge",
    "delbot_platform.knowledge.models",
    "delbot_platform.knowledge.rag",
]

for mod in modules:

    try:

        m = importlib.import_module(mod)

        print("[PASS]", mod)

    except Exception as e:

        print("[FAIL]", mod)
        print(type(e).__name__)
        print(e)

print()
print("=" * 70)
print("FIND DATACLASSES")
print("=" * 70)

for py in sorted(knowledge.rglob("*.py")):

    rel = py.relative_to(ROOT)

    try:
        tree = ast.parse(py.read_text(encoding="utf-8"))
    except Exception:
        continue

    dataclass = False

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            for dec in node.decorator_list:

                if isinstance(dec, ast.Name):
                    if dec.id == "dataclass":
                        dataclass = True

                elif isinstance(dec, ast.Call):
                    if isinstance(dec.func, ast.Name):
                        if dec.func.id == "dataclass":
                            dataclass = True

            if dataclass:

                print(rel)
                print("CLASS :", node.name)
                print()

print("=" * 70)
print("DONE")
print("=" * 70)
