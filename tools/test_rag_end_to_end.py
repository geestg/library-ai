from __future__ import annotations

import asyncio
import importlib
import inspect
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 70)
print("IMPORT")
print("=" * 70)

Retriever = importlib.import_module(
    "delbot_platform.knowledge.retrieval.qdrant"
).QdrantRetriever

ContextBuilder = importlib.import_module(
    "delbot_platform.knowledge.rag.context_builder"
).ContextBuilder

CitationBuilder = importlib.import_module(
    "delbot_platform.knowledge.rag.citation_builder"
).CitationBuilder

DocumentChunk = importlib.import_module(
    "delbot_platform.documents.models.document_chunk"
).DocumentChunk

print("Retriever      :", Retriever)
print("ContextBuilder :", ContextBuilder)
print("CitationBuilder:", CitationBuilder)

print()
print("=" * 70)
print("QUERY")
print("=" * 70)

QUERY = "PLC OMRON CPM2A dan Arduino Mega 2560"

print(QUERY)

retriever = Retriever()

start = time.time()

results = asyncio.run(
    retriever.retrieve(
        query=QUERY,
        limit=5,
    )
)

elapsed = time.time() - start

print()
print("=" * 70)
print("RETRIEVAL")
print("=" * 70)

print("COUNT :", len(results))
print("TIME  : %.2fs" % elapsed)

chunks = []

for r in results:

    meta = r.metadata

    chunk = DocumentChunk(
        document_id=meta.document_id,
        chunk_id=meta.chunk_id,
        page_start=meta.page_start,
        page_end=meta.page_end,
        section_title=meta.section_title,
        chapter=meta.chapter,
        text=r.content,
        metadata=meta,
        score=r.score,
    )

    chunks.append(chunk)

print()
print("=" * 70)
print("CONTEXT")
print("=" * 70)

context_builder = ContextBuilder()

context = context_builder.build(chunks)

print("TYPE   :", type(context).__name__)
print("LENGTH :", len(context))
print()
print(context[:2000])

print()
print("=" * 70)
print("CITATIONS")
print("=" * 70)

citation_builder = CitationBuilder()

citations = citation_builder.build(chunks)

print("COUNT :", len(citations))
print()

for i, c in enumerate(citations, 1):

    print(
        f"[{i}] "
        f"{c.document} | "
        f"page={c.page} | "
        f"score={c.score:.6f}"
    )

print()
print("=" * 70)
print("SIMULATED ANSWER")
print("=" * 70)

if chunks:

    answer = (
        "Berdasarkan dokumen repository, PLC OMRON CPM2A "
        "digunakan sebagai pengendali utama motor servo, "
        "sedangkan Arduino Mega 2560 digunakan untuk "
        "menjalankan algoritma fuzzy dan mengendalikan "
        "aktuator serta sensor. PLC menangani logika kontrol "
        "sementara Arduino menangani pemrosesan sensor dan "
        "pengendalian motor."
    )

    print(answer)

else:

    print("NO RESULT")

print()
print("=" * 70)
print("FINAL")
print("=" * 70)

print("Retriever :", "PASS" if results else "FAIL")
print("Context   :", "PASS" if isinstance(context, str) else "FAIL")
print("Citation  :", "PASS" if citations else "FAIL")
print("Pipeline  :", "PASS" if results and citations else "FAIL")
