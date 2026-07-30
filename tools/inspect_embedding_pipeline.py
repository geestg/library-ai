from __future__ import annotations

import inspect
import sys
from pathlib import Path
from dataclasses import fields, is_dataclass

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)

print("=" * 70)
print("EMBEDDING PIPELINE")
print("=" * 70)

print()
print("CLASS")
print(EmbeddingPipeline)

print()
print("=" * 70)
print("SIGNATURE")
print("=" * 70)

try:
    print(inspect.signature(EmbeddingPipeline))
except Exception as exc:
    print(exc)

print()
print("=" * 70)
print("METHODS")
print("=" * 70)

members = inspect.getmembers(
    EmbeddingPipeline,
    predicate=inspect.isfunction,
)

for name, fn in members:

    if name.startswith("__") and name != "__init__":
        continue

    print()
    print(name)

    try:
        print("SIGNATURE :", inspect.signature(fn))
    except Exception:
        pass

print()
print("=" * 70)
print("__INIT__ SOURCE")
print("=" * 70)

try:
    print(inspect.getsource(EmbeddingPipeline.__init__))
except Exception as exc:
    print(exc)

print()
print("=" * 70)
print("CLASS SOURCE")
print("=" * 70)

try:
    print(inspect.getsource(EmbeddingPipeline))
except Exception as exc:
    print(exc)

print()
print("=" * 70)
print("ASYNC CHECK")
print("=" * 70)

for name, fn in inspect.getmembers(EmbeddingPipeline):

    if inspect.iscoroutinefunction(fn):
        print("ASYNC :", name)

print()
print("=" * 70)
print("INSTANCE")
print("=" * 70)

pipe = EmbeddingPipeline()

print(type(pipe))

print()

print("PUBLIC ATTRIBUTES")

for name in sorted(dir(pipe)):

    if name.startswith("_"):
        continue

    obj = getattr(pipe, name)

    if callable(obj):
        continue

    print(name, "=", type(obj).__name__)

print()
print("=" * 70)
print("DONE")
print("=" * 70)
