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

print("=" * 70)
print("DOCUMENT CHUNK")
print("=" * 70)
print()

print("CLASS")
print(DocumentChunk)
print()

print("=" * 70)
print("SIGNATURE")
print("=" * 70)
print(inspect.signature(DocumentChunk))
print()

if is_dataclass(DocumentChunk):

    print("=" * 70)
    print("FIELDS")
    print("=" * 70)

    for field in fields(DocumentChunk):

        print(
            f"{field.name:<25}"
            f"type={field.type!s:<35}"
            f"default={field.default!r}"
        )

print()

print("=" * 70)
print("__INIT__ SOURCE")
print("=" * 70)

try:

    print(inspect.getsource(DocumentChunk.__init__))

except Exception as exc:

    print(exc)

print()

print("=" * 70)
print("CLASS SOURCE")
print("=" * 70)

try:

    print(inspect.getsource(DocumentChunk))

except Exception as exc:

    print(exc)

