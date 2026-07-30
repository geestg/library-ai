# DELBot Safe Removal Plan

## Summary

Modules : 470

| Action | Count |
|--------|------:|
| BLOCKED | 8 |
| KEEP | 359 |
| MANUAL | 43 |
| MERGE | 34 |
| SAFE_REMOVE | 26 |

## Candidates

| Module | Action | Incoming | Outgoing |
|--------|--------|---------:|---------:|
| delbot_platform.ai.registry.loader | BLOCKED | 1 | 0 |
| delbot_platform.config.loader | BLOCKED | 1 | 0 |
| delbot_platform.document_intelligence.loader.pdf_loader | BLOCKED | 1 | 0 |
| delbot_platform.documents.registry.manager | BLOCKED | 3 | 0 |
| delbot_platform.documents.registry.memory | BLOCKED | 1 | 0 |
| delbot_platform.gateway.providers.infinity | BLOCKED | 1 | 0 |
| delbot_platform.gateway.providers.vllm | BLOCKED | 1 | 0 |
| delbot_platform.gateway.routers.health | BLOCKED | 1 | 0 |
| delbot_platform.ai.client.embedding_client | MANUAL | 4 | 0 |
| delbot_platform.ai.embedding.embedding_builder | MANUAL | 0 | 0 |
| delbot_platform.ai.embedding.embedding_service | MANUAL | 0 | 0 |
| delbot_platform.api.research | MANUAL | 0 | 0 |
| delbot_platform.api.routers.document | MANUAL | 2 | 0 |
| delbot_platform.api.routers.research | MANUAL | 2 | 0 |
| delbot_platform.api.routes.document | MANUAL | 0 | 0 |
| delbot_platform.api.routes.research | MANUAL | 1 | 0 |
| delbot_platform.api.schemas.document | MANUAL | 1 | 0 |
| delbot_platform.api.schemas.research | MANUAL | 1 | 0 |
| delbot_platform.document_intelligence.builder.document_builder | MANUAL | 3 | 0 |
| delbot_platform.document_intelligence.loader.document_loader | MANUAL | 2 | 0 |
| delbot_platform.document_intelligence.models.block | MANUAL | 4 | 0 |
| delbot_platform.document_intelligence.parser.document_parser | MANUAL | 2 | 0 |
| delbot_platform.document_intelligence.pipeline.document_pipeline | MANUAL | 3 | 0 |
| delbot_platform.document_intelligence.processor.document_processor | MANUAL | 2 | 0 |
| delbot_platform.documents.extraction.block | MANUAL | 2 | 0 |
| delbot_platform.documents.metadata.builder.document | MANUAL | 2 | 0 |
| delbot_platform.documents.models.block | MANUAL | 8 | 0 |
| delbot_platform.documents.models.document | MANUAL | 2 | 0 |
| delbot_platform.documents.models.document_chunk | MANUAL | 8 | 0 |
| delbot_platform.documents.registry.document | MANUAL | 7 | 0 |
| delbot_platform.gateway.mapper.embedding | MANUAL | 2 | 0 |
| delbot_platform.gateway.openai.embedding | MANUAL | 2 | 0 |
| delbot_platform.gateway.response | MANUAL | 2 | 0 |
| delbot_platform.gateway.routers.embedding | MANUAL | 1 | 0 |
| delbot_platform.gateway.routers.research | MANUAL | 1 | 0 |
| delbot_platform.gateway.routers.v1.embedding | MANUAL | 0 | 0 |
| delbot_platform.knowledge.graph.graph_builder | MANUAL | 1 | 0 |
| delbot_platform.knowledge.models.document | MANUAL | 3 | 0 |
| delbot_platform.knowledge.models.document_chunk | MANUAL | 2 | 0 |
| delbot_platform.knowledge.rag.llm.response | MANUAL | 1 | 0 |
| delbot_platform.knowledge.rag.models.response | MANUAL | 4 | 0 |
| delbot_platform.knowledge.rag.research.response | MANUAL | 3 | 0 |
| delbot_platform.knowledge.reranking.result | MANUAL | 8 | 0 |
| delbot_platform.knowledge.retrieval.result | MANUAL | 3 | 0 |
| delbot_platform.orchestrator.services.embedding | MANUAL | 0 | 0 |
| tools.architecture.graph | MANUAL | 9 | 0 |
| delbot_platform.repository.download.result | MANUAL | 1 | 0 |
| delbot_platform.repository.integration.document_loader | MANUAL | 1 | 0 |
| delbot_platform.research.models.embedding | MANUAL | 4 | 0 |
| delbot_platform.research.research_engine | MANUAL | 5 | 0 |
| delbot_platform.workflows.repository.models.result | MANUAL | 0 | 0 |
| delbot_platform.api.routers.repository | MERGE | 2 | 0 |
| delbot_platform.api.schemas.repository | MERGE | 1 | 0 |
| delbot_platform.document_intelligence.models.heading | MERGE | 4 | 0 |
| delbot_platform.document_intelligence.models.page | MERGE | 5 | 0 |
| delbot_platform.documents.classification.heading | MERGE | 2 | 0 |
| delbot_platform.documents.embedding.providers.gateway | MERGE | 1 | 0 |
| delbot_platform.documents.embedding.providers.local | MERGE | 1 | 0 |
| delbot_platform.documents.loader.source | MERGE | 5 | 0 |
| delbot_platform.documents.loader.sources.local | MERGE | 2 | 0 |
| delbot_platform.documents.metadata.repository | MERGE | 1 | 0 |
| delbot_platform.documents.models.citation | MERGE | 0 | 0 |
| delbot_platform.documents.models.page | MERGE | 2 | 0 |
| delbot_platform.documents.registry.repository | MERGE | 4 | 0 |
| delbot_platform.gateway.client | MERGE | 3 | 0 |
| delbot_platform.gateway.mapper.chat | MERGE | 1 | 0 |
| delbot_platform.gateway.openai.chat | MERGE | 2 | 0 |
| delbot_platform.gateway.providers.local | MERGE | 1 | 0 |
| delbot_platform.gateway.routers.chat | MERGE | 1 | 0 |
| delbot_platform.gateway.routers.v1.chat | MERGE | 0 | 0 |
| delbot_platform.gateway.services.gateway | MERGE | 4 | 0 |
| delbot_platform.knowledge.citation.source | MERGE | 3 | 0 |
| delbot_platform.knowledge.hydration.citation | MERGE | 0 | 0 |
| delbot_platform.knowledge.hydration.local | MERGE | 0 | 0 |
| delbot_platform.knowledge.models.repository | MERGE | 1 | 0 |
| delbot_platform.knowledge.rag.citation_builder | MERGE | 0 | 0 |
| delbot_platform.knowledge.reranking.gateway | MERGE | 1 | 0 |
| delbot_platform.knowledge.reranking.local | MERGE | 0 | 0 |
| delbot_platform.orchestrator.services.gateway | MERGE | 0 | 0 |
| .backup.stage_4_24.gateway | MERGE | 0 | 0 |
| delbot_platform.research.llm.chat_client | MERGE | 0 | 0 |
| delbot_platform.research.llm.client | MERGE | 0 | 0 |
| delbot_platform.research.models.citation | MERGE | 4 | 0 |
| delbot_platform.vectorstore.qdrant.client | MERGE | 1 | 0 |
| delbot_platform.vectorstore.qdrant.repository | MERGE | 0 | 0 |
| delbot_platform.ai.client.reranker_client | SAFE_REMOVE | 0 | 0 |
| delbot_platform.ai.http.http_client | SAFE_REMOVE | 0 | 0 |
| delbot_platform.api.app | SAFE_REMOVE | 0 | 0 |
| delbot_platform.application.research.answer | SAFE_REMOVE | 0 | 0 |
| delbot_platform.config.manager | SAFE_REMOVE | 0 | 0 |
| delbot_platform.document_intelligence.mappermupdf_mapper | SAFE_REMOVE | 0 | 0 |
| delbot_platform.documents.parser.backendmupdf | SAFE_REMOVE | 0 | 0 |
| delbot_platform.documents.parser.pdf | SAFE_REMOVE | 0 | 0 |
| delbot_platform.documents.pipeline.models.artifact | SAFE_REMOVE | 0 | 0 |
| delbot_platform.gateway.app | SAFE_REMOVE | 0 | 0 |
| delbot_platform.gateway.routers.reranker | SAFE_REMOVE | 0 | 0 |
| delbot_platform.gateway.routers.vision | SAFE_REMOVE | 0 | 0 |
| delbot_platform.knowledge.pipeline.models.artifact | SAFE_REMOVE | 0 | 0 |
| delbot_platform.knowledge.rag.context_builder | SAFE_REMOVE | 0 | 0 |
| delbot_platform.knowledge.rerank.reranker | SAFE_REMOVE | 0 | 0 |
| delbot_platform.knowledge.vector.repository.memory | SAFE_REMOVE | 0 | 0 |
| delbot_platform.launcher.infinity | SAFE_REMOVE | 0 | 0 |
| delbot_platform.launcher.vllm | SAFE_REMOVE | 0 | 0 |
| delbot_platform.orchestrator.health | SAFE_REMOVE | 0 | 0 |
| delbot_platform.orchestrator.services.reranker | SAFE_REMOVE | 0 | 0 |
| delbot_platform.orchestrator.services.vision | SAFE_REMOVE | 0 | 0 |
| delbot_platform.repository.catalog.loader | SAFE_REMOVE | 0 | 0 |
| delbot_platform.repository.discovery.http | SAFE_REMOVE | 0 | 0 |
| delbot_platform.research.rag.context | SAFE_REMOVE | 0 | 0 |
| delbot_platform.research.services.answer | SAFE_REMOVE | 0 | 0 |
| delbot_platform.workflows.repository.models.artifact | SAFE_REMOVE | 0 | 0 |