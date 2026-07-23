from __future__ import annotations

from delbot_platform.ai.client.llm_client import LLMClient
from delbot_platform.knowledge.models import (
    Author,
    RAGResult,
)
from delbot_platform.knowledge.rag.rag_engine import RAGEngine
from delbot_platform.research.memory.research_memory import (
    ResearchMemory,
)
from delbot_platform.research.models import Citation
from delbot_platform.research.models import ResearchResult
from delbot_platform.research.prompt_builder import (
    ResearchPromptBuilder,
)
from delbot_platform.workspace.session_manager import (
    SessionManager,
)


class ResearchEngine:

    def __init__(
        self,
        session_manager: SessionManager,
    ) -> None:

        self.sessions = session_manager
        self.rag = RAGEngine()
        self.llm = LLMClient()
        self.builder = ResearchPromptBuilder()
        self.memory = ResearchMemory()

    def ask(
        self,
        session_id: str,
        query: str,
        history: list[dict] | None = None,
    ) -> ResearchResult:

        history = history or []

        session = self.sessions.get_object(
            session_id
        )

        if session is None:

            raise ValueError(
                f"Session '{session_id}' not found."
            )

        state = session.research_state

        state.update_question(
            query
        )

        rag_result: RAGResult = (
            self.rag.search(
                query
            )
        )

        context = rag_result.context

        citations: list[Citation] = (
            rag_result.citations
        )

        memory = self.memory.load(
            session_id
        )

        messages = self.builder.build(
            query=query,
            context=context,
            history=history,
            previous=memory.get(
                "last_answer",
                "",
            ),
            research_state=state.export(),
        )

        answer = self.llm.chat(
            messages
        )

        state.update_answer(
            answer
        )

        for citation in citations:

            state.add_source(
                citation
            )

        self.sessions.replace_state(
            session_id,
            state,
        )

        exported_state = state.export()

        authors: list[Author] = []
        author_ids: list[str] = []
        author_names: list[str] = []

        seen_author_ids: set[str] = set()

        for citation in citations:

            for author in citation.authors:

                if author.author_id in seen_author_ids:
                    continue

                seen_author_ids.add(
                    author.author_id
                )

                authors.append(
                    author
                )

                author_ids.append(
                    author.author_id
                )

                author_names.append(
                    author.full_name
                )

        self.memory.save(
            session_id=session_id,
            query=query,
            answer=answer,
            research_state=exported_state,
            summary=exported_state.get(
                "summary",
                "",
            ),
            keywords=exported_state.get(
                "keywords",
                [],
            ),
            sources=exported_state.get(
                "sources",
                [],
            ),
            notes=exported_state.get(
                "notes",
                [],
            ),
            timeline=exported_state.get(
                "timeline",
                [],
            ),
        )

        return ResearchResult(
            answer=answer,
            sources=citations,
            authors=authors,
            author_ids=author_ids,
            author_names=author_names,
            research_state=exported_state,
        )