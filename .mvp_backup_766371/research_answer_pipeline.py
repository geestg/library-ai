from __future__ import annotations

import re

import inspect

from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)

from delbot_platform.repository.service import (
    RepositoryService,
)

from delbot_platform.research.generator import (
    LLMGenerator,
)

from delbot_platform.research.models import (
    ResearchPipelineResponse,
)

from delbot_platform.research.prompt_builder import (
    ResearchPromptBuilder,
)


class ResearchAnswerPipeline:

    def __init__(
        self,
    ) -> None:

        self.rag = None

        self.prompt_builder = (
            ResearchPromptBuilder()
        )

        self.generator = (
            LLMGenerator()
        )

        self._last_discovery_candidates = []

    def _contains_term(
        self,
        text: str,
        term: str,
    ) -> bool:

        pattern = (
            r"(?<!\\w)"
            + re.escape(term)
            + r"(?!\\w)"
        )

        return re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ) is not None

    def _is_research_turn(
        self,
        question: str,
        history: list[dict],
        research_state: dict | None = None,
    ) -> bool:

        text = question.lower().strip()
        state = research_state or {}

        research_terms = (
            "research",
            "penelitian",
            "meneliti",
            "riset",
            "skripsi",
            "tesis",
            "thesis",
            "jurnal",
            "paper",
            "literatur",
            "literature review",
            "akademik",
            "metode penelitian",
            "metodologi",
            "research gap",
            "research question",
            "thesis idea",
            "ide penelitian",
        )

        if any(
            term in text
            for term in research_terms
        ):
            return True

        topic_terms = (
            "computer vision",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "kecerdasan buatan",
            "natural language processing",
            "data science",
            "robotics",
            "internet of things",
        )

        has_topic_selection = any(
            term in text
            for term in topic_terms
        )

        has_research_context = bool(
            state.get("topic")
            or state.get("research_direction")
            or any(
                any(
                    term in str(
                        item.get("content", "")
                    ).lower()
                    for term in research_terms
                )
                for item in history[-8:]
            )
        )

        topic_selection_terms = (
            "menarik",
            "tertarik",
            "pilih",
            "memilih",
            "minat",
            "berminat",
            "suka",
            "ingin",
            "mau",
        )

        has_topic_selection_intent = any(
            term in text
            for term in topic_selection_terms
        )

        if (
            has_topic_selection
            and (
                has_research_context
                or has_topic_selection_intent
            )
        ):
            return True

        context_terms = (
            "yang tadi",
            "tadi",
            "sebelumnya",
            "tersebut",
            "yang kita bahas",
            "arah itu",
            "topik itu",
            "lanjutkan",
            "lanjut",
        )

        has_research_context = (
            state.get("topic")
            or state.get("research_direction")
        )

        if (
            has_research_context
            and any(
                self._contains_term(
                    text,
                    term,
                )
                for term in context_terms
            )
        ):
            return True

        research_history_terms = (
            "penelitian",
            "meneliti",
            "riset",
            "research",
            "thesis",
            "skripsi",
            "tesis",
            "jurnal",
            "paper",
            "literatur",
            "akademik",
            "research gap",
            "thesis idea",
        )

        for item in history[-8:]:
            content = str(
                item.get("content", "")
            ).lower()

            if any(
                term in content
                for term in research_history_terms
            ):
                return True

        return False

    def _requires_evidence(
        self,
        question: str,
        history: list[dict],
        research_state: dict,
    ) -> bool:

        text = question.lower().strip()

        evidence_terms = (
            "berdasarkan repository",
            "berdasarkan penelitian",
            "berdasarkan literatur",
            "berdasarkan jurnal",
            "berdasarkan dokumen",
            "dari repository",
            "dari penelitian",
            "dari literatur",
            "dari jurnal",
            "dari dokumen",
            "di repository",
            "di dataset",
            "penelitian yang relevan",
            "literatur yang relevan",
            "dokumen yang relevan",
            "sumber penelitian",
            "sumbernya",
            "citation",
            "citation",
            "sitasi",
            "evidence",
            "bukti",
            "research gap",
            "research gap",
            "gap penelitian",
            "thesis idea",
            "thesis ideas",
            "ide skripsi",
            "ide tesis",
            "ide penelitian",
            "berikan ide penelitian",
            "beri ide penelitian",
            "literature review",
            "tinjauan literatur",
            "bandingkan penelitian",
            "bandingkan jurnal",
            "compare penelitian",
            "comparison",
            "keterbatasan penelitian",
            "limitations",
            "future work",
            "recommendation",
        )

        if any(
            term in text
            for term in evidence_terms
        ):
            return True

        topic = (
            research_state.get("topic")
            or research_state.get("research_direction")
        )

        if not topic:
            return False

        discovery_terms = (
            "apa yang ada",
            "apa saja",
            "penelitian apa",
            "penelitian yang ada",
            "yang relevan",
            "yang tersedia",
            "contoh penelitian",
            "penelitian terkait",
            "literatur terkait",
            "jurnal terkait",
        )

        if any(
            term in text
            for term in discovery_terms
        ):
            return True

        continuation_terms = (
            "yang tadi",
            "tadi",
            "sebelumnya",
            "tersebut",
            "yang kita bahas",
            "arah itu",
            "topik itu",
        )

        if any(
            term in text
            for term in continuation_terms
        ):
            return True

        return False

    def _evolve_research_state(
        self,
        *,
        question: str,
        history: list[dict],
        previous: str,
        research_state: dict,
        research_turn: bool,
    ) -> dict:
        state = dict(research_state or {})

        keywords = list(
            state.get("keywords") or []
        )

        text = question.strip()
        lowered = text.lower()

        topic_terms = (
            "computer vision",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai",
            "kecerdasan buatan",
            "natural language processing",
            "nlp",
            "llm",
            "iot",
            "internet of things",
            "robotics",
            "data science",
        )

        detected_topic = None

        for term in topic_terms:
            if term in lowered:
                detected_topic = term
                break

        if detected_topic:
            state["topic"] = detected_topic

            if detected_topic not in keywords:
                keywords.append(detected_topic)

        research_goal_terms = (
            "meneliti",
            "penelitian",
            "riset",
            "research",
            "skripsi",
            "tesis",
            "thesis",
            "research gap",
            "thesis idea",
            "ide penelitian",
        )

        if any(
            term in lowered
            for term in research_goal_terms
        ):
            state["research_goal"] = text

        if research_turn:
            state["current_question"] = text

        if previous:
            state["current_answer"] = previous

        state["keywords"] = keywords

        if detected_topic:
            state["research_direction"] = detected_topic

        if research_turn:
            timeline = list(
                state.get("timeline") or []
            )

            timeline.append(
                {
                    "event": "research_turn",
                    "value": text,
                }
            )

            state["timeline"] = timeline[-20:]

        return state

    def _build_metadata_discovery_context(
        self,
        topic: str,
        limit: int = 8,
    ) -> str:

        if not topic:
            return ""

        try:
            items = RepositoryService().scan()
        except Exception:
            return ""

        topic_terms = [
            term.strip().lower()
            for term in topic.split()
            if term.strip()
        ]

        if not topic_terms:
            return ""

        scored = []

        for item in items:
            metadata = getattr(
                item,
                "metadata",
                {},
            ) or {}

            title = str(
                getattr(item, "title", "")
                or ""
            )

            abstract = str(
                metadata.get("abstract", "")
                or ""
            )

            author = str(
                metadata.get("author", "")
                or ""
            )

            year = str(
                metadata.get("year", "")
                or ""
            )

            searchable = (
                f"{title} {abstract} "
                f"{author} {year}"
            ).lower()

            score = sum(
                1
                for term in topic_terms
                if term in searchable
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        title,
                        author,
                        year,
                        abstract,
                        getattr(item, "id", ""),
                        bool(
                            metadata.get("has_pdf")
                        ),
                    )
                )

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].lower(),
            )
        )

        selected = scored[:limit]

        self._last_discovery_candidates = [
            {
                "document_id": item[5],
                "title": item[1],
                "author": item[2],
                "year": item[3],
                "has_pdf": item[6],
            }
            for item in selected
        ]

        if not selected:
            return ""

        state = getattr(
            self,
            "_active_research_state",
            None,
        )

        if isinstance(state, dict):
            state["discovery_topic"] = topic

            discovered_documents = []

            for row in selected:
                (
                    score,
                    title,
                    author,
                    year,
                    abstract,
                    document_id,
                    has_pdf,
                ) = row

                discovered_documents.append(
                    {
                        "document_id": document_id,
                        "title": title,
                        "author": author,
                        "year": year,
                        "abstract": abstract,
                        "has_pdf": has_pdf,
                    }
                )

            state["discovered_documents"] = (
                discovered_documents[:limit]
            )

        context = [
            "REPOSITORY DISCOVERY",
            f"Research direction: {topic}",
            "The following metadata/abstract records "
            "are discovery candidates only.",
            "Do not treat metadata or abstract as "
            "fulltext evidence.",
            "",
        ]

        for index, item in enumerate(
            selected,
            start=1,
        ):
            (
                score,
                title,
                author,
                year,
                abstract,
                document_id,
                has_pdf,
            ) = item

            context.append(
                f"[Candidate {index}]"
            )
            context.append(
                f"Document ID: {document_id}"
            )
            context.append(
                f"Title: {title}"
            )
            context.append(
                f"Author: {author}"
            )
            context.append(
                f"Year: {year}"
            )
            context.append(
                f"Has PDF: {has_pdf}"
            )
            context.append(
                f"Abstract: {abstract[:900]}"
            )
            context.append("")

        return "\n".join(context)

    def get_rag(
        self,
    ) -> RAGPipeline:

        if self.rag is None:

            self.rag = RAGPipeline()

        return self.rag

    async def answer(
        self,
        *,
        question: str,
        history: list[dict] | None = None,
        previous: str = "",
        research_state: dict | None = None,
    ) -> ResearchPipelineResponse:

        history = history or []

        research_state = (
            research_state or {}
        )

        research_turn = self._is_research_turn(
            question,
            history,
            research_state,
        )

        research_state = self._evolve_research_state(
            question=question,
            history=history,
            previous=previous,
            research_state=research_state,
            research_turn=research_turn,
        )

        self._active_research_state = research_state

        evidence_turn = self._requires_evidence(
            question,
            history,
            research_state,
        )

        if (
            research_turn
            and not evidence_turn
        ):
            discovery_topic = (
                research_state.get("topic")
                or research_state.get(
                    "research_direction"
                )
                or ""
            )

            discovery_context = (
                self._build_metadata_discovery_context(
                    discovery_topic
                )
            )

            discovered = list(
                self._last_discovery_candidates
                or []
            )

            if discovered:
                research_state[
                    "discovered_documents"
                ] = discovered[:8]

                research_state[
                    "discovery_topic"
                ] = discovery_topic

        else:
            discovery_context = ""

        if evidence_turn:

            topic = (
                research_state.get("topic")
                or research_state.get("research_direction")
                or ""
            )

            research_gap = (
                research_state.get("research_gap")
                or ""
            )

            thesis_idea = (
                research_state.get("thesis_idea")
                or ""
            )

            continuation_terms = (
                "yang tadi",
                "tadi",
                "sebelumnya",
                "tersebut",
                "yang kita bahas",
                "arah itu",
                "topik itu",
            )

            is_continuation = any(
                term in question.lower()
                for term in continuation_terms
            )

            discovered_documents = list(
                research_state.get(
                    "discovered_documents"
                )
                or []
            )

            if is_continuation and topic:
                rag_query = (
                    f"Research topic: {topic}. "
                    f"User follow-up: {question}"
                )

                if discovered_documents:
                    document_ids = [
                        str(item.get("document_id", ""))
                        for item in discovered_documents
                        if item.get("document_id")
                    ]

                    if document_ids:
                        rag_query += (
                            " Candidate document IDs: "
                            + ", ".join(document_ids)
                        )

                if research_gap:
                    rag_query += (
                        f" Research gap: {research_gap}"
                    )

                if thesis_idea:
                    rag_query += (
                        f" Thesis idea: {thesis_idea}"
                    )
            else:
                rag_query = question

            rag = await self.get_rag().build(
                query=rag_query,
            )

            context = rag.context
            citations = rag.citations

            persisted_sources = list(
                research_state.get("sources") or []
            )

            for citation in citations:
                if hasattr(citation, "to_dict"):
                    source = citation.to_dict()
                elif hasattr(citation, "export"):
                    source = citation.export()
                elif isinstance(citation, dict):
                    source = citation
                else:
                    source = str(citation)

                if source not in persisted_sources:
                    persisted_sources.append(source)

            research_state["sources"] = (
                persisted_sources[-20:]
            )

        else:


            rag = None
            context = ""
            citations = []

        if discovery_context:
            if context:
                context = (
                    discovery_context
                    + "\n\n"
                    + context
                )
            else:
                context = discovery_context

        messages = (
            self.prompt_builder.build(
                query=question,
                context=context,
                history=history,
                previous=previous,
                research_state=research_state,
                mode=(
                    "research"
                    if evidence_turn
                    else "conversation"
                ),
            )
        )

        generated = self.generator.generate(
            messages,
        )

        if inspect.isawaitable(
            generated
        ):
            generated = await generated

        research_state["current_answer"] = generated

        question_lower = question.lower()

        gap_signals = (
            "research gap",
            "gap penelitian",
            "kesenjangan penelitian",
            "research gaps",
            "gap riset",
            "keterbatasan penelitian",
        )

        thesis_signals = (
            "thesis idea",
            "thesis ideas",
            "ide skripsi",
            "ide tesis",
            "ide penelitian",
            "topik skripsi",
            "topik tesis",
        )

        if any(
            signal in question_lower
            for signal in gap_signals
        ):
            research_state["research_gap"] = generated

        if any(
            signal in question_lower
            for signal in thesis_signals
        ):
            research_state["thesis_idea"] = generated

        self._active_research_state = None

        return ResearchPipelineResponse(
            answer=generated,
            citations=citations,
            research_state=research_state,
            rag=rag,
        )
