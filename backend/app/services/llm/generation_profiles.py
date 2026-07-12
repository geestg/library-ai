from app.services.llm.models.execution_config import (
    ExecutionConfig,
)


class GenerationProfiles:

    # klasifikasi ya/tidak
    VERIFIER = ExecutionConfig(
        temperature=0,
        max_tokens=8,
    )

    # jawaban RAG normal
    ANSWER = ExecutionConfig(
        temperature=0,
    )

    # rewrite query
    QUERY_RESOLUTION = ExecutionConfig(
        temperature=0,
        max_tokens=32,
    )

    # judul chat
    TITLE = ExecutionConfig(
        temperature=0.3,
        max_tokens=32,
    )

    # literature review
    RESEARCH = ExecutionConfig(
        temperature=0.2,
    )

    # brainstorming
    CREATIVE = ExecutionConfig(
        temperature=0.7,
    )