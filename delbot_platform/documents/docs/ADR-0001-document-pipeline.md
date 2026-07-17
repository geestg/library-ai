# ADR-0001 — Document Pipeline V2

Status: Accepted

Date: 2026-07-17

---

# Context

The document module has evolved from multiple experimental implementations into a
single production-oriented PDF-first architecture.

During development several legacy components remained in the repository.

Examples:

- structure/builder.py
- structure/hierarchy.py
- structure/section_node.py
- chunking/builder.py
- loader/pdf.py

These components belong to the previous indexing architecture and are no longer
the target architecture.

This ADR defines the canonical document indexing pipeline.

---

# Goals

The pipeline must satisfy the following principles.

1. PDF First

The PDF document is the primary source of truth.

Metadata is supplementary only.

---

2. Stateless Processing

Each pipeline stage performs one responsibility.

Stages communicate only through immutable domain models.

---

3. Single Responsibility

Each component owns exactly one concern.

Example

DocumentExtractionService

- Open PDF
- Extract layout blocks

NOT

- Build sections
- Build chunks
- Create embeddings

---

4. Orchestration

DocumentIndexingPipeline coordinates execution.

Business logic must remain inside individual services.

---

# Canonical Pipeline

```
PDF

↓

DocumentRegistryManager

↓

DocumentPreprocessingPipeline

↓

DocumentExtractionService

↓

HeadingClassifier

↓

SectionBuilder

↓

ChunkBuilder

↓

EmbeddingPipeline

↓

Vector Store

↓

Research Retrieval
```

---

# Canonical Domain Models

```
Block

↓

DocumentSection

↓

DocumentChunk

↓

ChunkMetadata

↓

VectorRecord
```

No other models should be introduced for the same responsibilities.

---

# Dependency Rules

Allowed

```
Pipeline
    ↓

Services
    ↓

Models
```

Forbidden

```
Pipeline

↓

PyMuPDF

↓

Raw dictionaries

↓

Manual parsing
```

---

# Legacy Components

The following modules are deprecated.

```
documents/structure/builder.py

documents/structure/hierarchy.py

documents/structure/section_node.py

documents/chunking/builder.py

documents/loader/pdf.py
```

They remain temporarily until migration completes.

No new code may depend on them.

---

# Future Work

After migration completes

- remove deprecated modules
- remove obsolete tests
- remove obsolete imports
- simplify package exports

---

End of ADR-0001