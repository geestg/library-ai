# ADR-001
# Canonical RAG Data Model

Status: Proposed

## Context

DELBot currently contains two different RAG output models:

Legacy

    RAGEngine
        ↓
    RAGResult

Modern

    RAGPipeline
        ↓
    RAGResponse

The coexistence of two output contracts prevents ResearchEngine from
switching to the new pipeline without adapters.

## Decision

DELBot SHALL expose exactly one canonical RAG output model.

The canonical model replaces RAGResponse.

Future RAGPipeline implementations SHALL return the canonical model.

## Canonical Flow

ResearchEngine
    ↓
RAGPipeline
    ↓
Retriever
    ↓
Reranker
    ↓
Context Builder
    ↓
Citation Builder
    ↓
Canonical RAGResult

## Consequences

Positive

- Single output contract
- Easier testing
- Easier caching
- Easier streaming
- Simpler maintenance

Negative

- Requires migration of:
  - ResearchEngine
  - RAGPipeline
  - ContextBuilder
  - CitationBuilder

