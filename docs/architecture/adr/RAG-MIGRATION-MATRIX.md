# Canonical RAG Migration Matrix

| Legacy | Canonical | Status |
|---------|-----------|--------|
| knowledge/rag/rag_engine.py | knowledge/rag/pipeline.py | Planned |
| knowledge/rag/vector_retriever.py | knowledge/retrieval/qdrant.py | Planned |
| knowledge/rag/context_builder.py | knowledge/context/builder.py | Planned |
| knowledge/rag/citation_builder.py | knowledge/citation/builder.py | Planned |
| ai/client/reranker_client.py | knowledge/reranking/gateway.py | Planned |

Migration Order

1. Canonical Data Model
2. Retrieval
3. Context
4. Citation
5. Pipeline
6. ResearchEngine
7. Legacy Removal

