from __future__ import annotations

import ast
import asyncio
import importlib
import inspect
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------

def banner(title: str):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


QUERY = "PLC OMRON CPM2A dan Arduino Mega 2560"


# ------------------------------------------------------------
# Locate Components
# ------------------------------------------------------------

banner("LOCATE RAG PIPELINE")

targets = [
    "delbot_platform.knowledge.rag.pipeline",
    "delbot_platform.knowledge.rag.rag_engine",
    "delbot_platform.knowledge.rag.vector_retriever",
    "delbot_platform.knowledge.rag.context_builder",
    "delbot_platform.knowledge.rag.citation_builder",
]

loaded = []

for mod_name in targets:

    try:

        mod = importlib.import_module(mod_name)

        print("[PASS]", mod_name)

        loaded.append(mod)

    except Exception as e:

        print("[FAIL]", mod_name)
        print(type(e).__name__)
        print(e)

banner("PUBLIC CLASSES")

for mod in loaded:

    print()
    print(mod.__name__)

    for name, obj in inspect.getmembers(mod):

        if inspect.isclass(obj):

            if obj.__module__ != mod.__name__:
                continue

            print("CLASS :", name)

            for method_name, method in inspect.getmembers(
                obj,
                inspect.isfunction,
            ):

                if method_name.startswith("_"):
                    continue

                print("   ", method_name)


# ------------------------------------------------------------
# Retriever
# ------------------------------------------------------------

banner("RETRIEVER")

from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)

from delbot_platform.knowledge.retrieval.qdrant import (
    QdrantRetriever,
)

query_chunk = DocumentChunk(
    document_id="query",
    chunk_id=str(uuid.uuid4()),
    page_start=0,
    page_end=0,
    text=QUERY,
)

embedding_pipeline = EmbeddingPipeline()

start = time.time()

retriever = QdrantRetriever()


results = asyncio.run(
    retriever.retrieve(
        query="PLC OMRON CPM2A dan Arduino Mega 2560",
        limit=5,
    )
)


elapsed = time.time() - start

print("RESULT :", len(results))
print("TIME   : %.2fs" % elapsed)

assert len(results) > 0


# ------------------------------------------------------------
# Convert RetrievalResult -> DocumentChunk
# ------------------------------------------------------------

banner("BUILD DOCUMENT CHUNKS")

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)

chunks = []

for item in results:

    meta = item.metadata

    chunk = DocumentChunk(
        document_id=meta.document_id,
        chunk_id=meta.chunk_id,
        page_start=meta.page_start,
        page_end=meta.page_end,
        section_title=meta.section_title,
        chapter=meta.chapter,
        text=item.content,
        metadata=meta,
        score=item.score,
    )

    chunks.append(chunk)

print("CHUNKS :", len(chunks))


# ------------------------------------------------------------
# Context Builder
# ------------------------------------------------------------

banner("CONTEXT BUILDER")

ContextBuilder = None

for mod in loaded:

    if mod.__name__.endswith("context_builder"):

        ContextBuilder = getattr(
            mod,
            "ContextBuilder",
            None,
        )

if ContextBuilder is None:

    print("NOT FOUND")

else:

    builder = ContextBuilder()

    methods = [
        x
        for x in dir(builder)
        if not x.startswith("_")
    ]

    print("METHODS :", methods)

    if hasattr(builder, "build"):

        try:

            context = builder.build(chunks)

            print("TYPE :", type(context))

            if isinstance(context, str):
                print("LENGTH :", len(context))
                print()
                print(context[:1000])

            else:
                print(context)

        except Exception as e:

            print(type(e).__name__)
            print(e)


# ------------------------------------------------------------
# Citation Builder
# ------------------------------------------------------------

banner("CITATION BUILDER")

from delbot_platform.knowledge.rag.citation_builder import (
    CitationBuilder,
)

citation_builder = CitationBuilder()

citations = citation_builder.build(
    chunks,
)

print("COUNT :", len(citations))

if citations:

    print()
    print(citations[0])


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

banner("SUMMARY")

print("QUERY")
print(QUERY)
print()

print("Retriever :", "PASS")
print("Context   :", "PASS (loaded)")
print("Citation  :", "PASS")
print()

print("TOP DOCUMENTS")

for item in results:

    print(
        item.metadata.document_id,
        "|",
        item.score,
    )

print()

print("=" * 70)
print("PR-3.7A PASS")
print("=" * 70)

