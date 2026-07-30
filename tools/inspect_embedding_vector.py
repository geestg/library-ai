from __future__ import annotations

import inspect
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)

print("=" * 70)
print("BUILD SAMPLE EMBEDDING")
print("=" * 70)


async def main():

    import asyncio
    import uuid

    pipeline = EmbeddingPipeline()

    chunk = DocumentChunk(
        document_id="debug",
        chunk_id=str(uuid.uuid4()),
        page_start=1,
        page_end=1,
        text="PLC OMRON CPM2A dan Arduino Mega 2560",
    )

    vectors = await pipeline.run([chunk])

    vector = vectors[0]

    print()
    print("=" * 70)
    print("CLASS")
    print("=" * 70)
    print(type(vector))

    print()
    print("=" * 70)
    print("SIGNATURE")
    print("=" * 70)
    print(inspect.signature(type(vector)))

    print()
    print("=" * 70)
    print("FIELDS")
    print("=" * 70)

    if is_dataclass(vector):

        for f in fields(vector):
            value = getattr(vector, f.name)

            typename = type(value).__name__

            if isinstance(value, list):
                preview = f"list(len={len(value)})"
            elif isinstance(value, str):
                preview = value[:80]
            else:
                preview = repr(value)

            print(
                f"{f.name:<24}"
                f"type={typename:<18}"
                f"value={preview}"
            )

    else:
        print("NOT DATACLASS")

    print()
    print("=" * 70)
    print("PUBLIC ATTRIBUTES")
    print("=" * 70)

    attrs = []

    for name in dir(vector):

        if name.startswith("_"):
            continue

        try:
            value = getattr(vector, name)
        except Exception:
            continue

        if callable(value):
            continue

        attrs.append(name)

    for name in sorted(attrs):

        try:
            value = getattr(vector, name)

            if isinstance(value, list):
                preview = f"list(len={len(value)})"
            elif isinstance(value, str):
                preview = value[:80]
            else:
                preview = repr(value)

            print(f"{name:<24}{preview}")

        except Exception as exc:
            print(f"{name:<24}ERROR {exc}")

    print()
    print("=" * 70)
    print("PUBLIC METHODS")
    print("=" * 70)

    methods = []

    for name in dir(vector):

        if name.startswith("_"):
            continue

        obj = getattr(vector, name)

        if callable(obj):
            methods.append(name)

    for m in sorted(methods):
        try:
            print(f"{m:<24}{inspect.signature(getattr(vector,m))}")
        except Exception:
            print(m)

    print()
    print("=" * 70)
    print("RAW OBJECT")
    print("=" * 70)
    print(vector)

import asyncio
asyncio.run(main())
