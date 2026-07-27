# RAG V2 Status

Status:
FROZEN

Reason:
The asynchronous RAG pipeline is intentionally frozen until the MVP Thesis
Edition is completed.

Current Canonical Pipeline:

ResearchEngine
    ↓
RAGEngine
    ↓
RAGPipeline
    ↓
VectorRetriever
    ↓
RerankerClient
    ↓
ContextBuilder
    ↓
CitationBuilder
    ↓
RAGResult

Experimental Components (Do Not Extend)

knowledge/rag/pipeline.py

knowledge/rag/research/

knowledge/rag/models/response.py

These components remain in the repository only for future migration after the
MVP is declared complete.
