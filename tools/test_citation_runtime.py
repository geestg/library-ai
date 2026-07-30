from __future__ import annotations

import ast
import asyncio
import importlib
import inspect
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


print("=" * 70)
print("LOCATE CITATION")
print("=" * 70)

citation_cls = None

for py in ROOT.rglob("*.py"):

    if ".venv" in py.parts:
        continue

    try:
        tree = ast.parse(py.read_text(encoding="utf-8"))
    except Exception:
        continue

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            if node.name != "Citation":
                continue

            module = (
                ".".join(py.relative_to(ROOT).with_suffix("").parts)
            )

            print(module)

            mod = importlib.import_module(module)

            citation_cls = getattr(mod, "Citation")

            print()
            print(inspect.signature(citation_cls))

            break

if citation_cls is None:
    print()
    print("NO Citation DATACLASS FOUND")
    raise SystemExit


print()
print("=" * 70)
print("BUILD DOCUMENT CHUNK")
print("=" * 70)

from delbot_platform.documents.models.document_chunk import DocumentChunk
from delbot_platform.documents.metadata.chunk_metadata import ChunkMetadata

metadata = ChunkMetadata(
    document_id="demo",
    chunk_id="chunk-demo",
    source="demo.pdf",
    page_start=10,
    page_end=12,
)

chunk = DocumentChunk(
    document_id="demo",
    chunk_id=str(uuid.uuid4()),
    page_start=10,
    page_end=12,
    section_title="Introduction",
    text="PLC OMRON CPM2A dan Arduino Mega 2560",
    metadata=metadata,
)

chunk.score = 0.987


print("=" * 70)
print("IMPORT CitationBuilder")
print("=" * 70)

builder_module = importlib.import_module(
    "delbot_platform.knowledge.rag.citation_builder"
)

CitationBuilder = getattr(
    builder_module,
    "CitationBuilder",
)

builder = CitationBuilder()

print(builder.__class__.__name__)


print()
print("=" * 70)
print("BUILD")
print("=" * 70)

result = builder.build([chunk])

print(type(result))
print("COUNT :", len(result))
print()

for item in result:
    print(item)

print()
print("=" * 70)
print("PASS")
print("=" * 70)
