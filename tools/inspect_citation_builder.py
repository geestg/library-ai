from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path
from dataclasses import fields, is_dataclass

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print("=" * 70)
print("LOCATE CITATION BUILDER")
print("=" * 70)

module = importlib.import_module(
    "delbot_platform.knowledge.rag.citation_builder"
)

CitationBuilder = getattr(
    module,
    "CitationBuilder",
)

print()
print("MODULE")
print(module.__name__)

print()
print("CLASS")
print(CitationBuilder)

print()
print("=" * 70)
print("SIGNATURE")
print("=" * 70)

print(
    inspect.signature(
        CitationBuilder
    )
)

print()
print("=" * 70)
print("PUBLIC METHODS")
print("=" * 70)

for name, member in inspect.getmembers(
    CitationBuilder,
):
    if name.startswith("_"):
        continue

    if inspect.isfunction(member) or inspect.ismethod(member):
        print()
        print(name)
        print(
            inspect.signature(
                member
            )
        )

print()
print("=" * 70)
print("__INIT__ SOURCE")
print("=" * 70)

try:
    print(
        inspect.getsource(
            CitationBuilder.__init__
        )
    )
except Exception as e:
    print(e)

print()
print("=" * 70)
print("BUILD SOURCE")
print("=" * 70)

try:
    print(
        inspect.getsource(
            CitationBuilder.build
        )
    )
except Exception as e:
    print(e)

print()
print("=" * 70)
print("CLASS SOURCE")
print("=" * 70)

try:
    print(
        inspect.getsource(
            CitationBuilder
        )
    )
except Exception as e:
    print(e)

print()
print("=" * 70)
print("INSTANCE")
print("=" * 70)

instance = CitationBuilder()

print(type(instance))

print()

for name in sorted(dir(instance)):
    if name.startswith("_"):
        continue

    try:
        value = getattr(
            instance,
            name,
        )

        if callable(value):
            continue

        print(
            f"{name} = {type(value).__name__}"
        )

    except Exception:
        pass

print()
print("=" * 70)
print("DONE")
print("=" * 70)
