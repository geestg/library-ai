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

        academic_evidence_terms = (
            "apa yang dimaksud",
            "apa itu",
            "pengertian",
            "definisi",
            "arti",
            "makna",
            "jelaskan",
            "jelaskan pengertian",
            "jelaskan definisi",
            "bagaimana cara",
            "bagaimana metode",
            "metode penelitian",
            "metodologi penelitian",
            "pengumpulan data",
            "analisis data",
            "hasil penelitian",
            "tujuan penelitian",
            "variabel penelitian",
            "instrumen penelitian",
            "dataset penelitian",
            "arsitektur",
            "algoritma",
            "model cnn",
            "computer vision",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "kecerdasan buatan",
            "yolo",
            "arduino",
            "raspberry pi",
            "plc omron",
        )

        if any(
            term in text
            for term in academic_evidence_terms
        ):
            return True

        follow_up_evidence_terms = (
            "keterbatasan",
            "kelebihan",
            "kekurangan",
            "hasilnya",
            "metodenya",
            "metode tersebut",
            "temuan tersebut",
            "hasil tersebut",
            "penelitian tersebut",
            "dokumen tersebut",
            "hal tersebut",
        )

        continuation_terms = (
            "tersebut",
            "itu",
            "tadi",
            "sebelumnya",
            "yang tadi",
            "yang dimaksud",
            "yang kita bahas",
        )

        has_follow_up_evidence = any(
            term in text
            for term in follow_up_evidence_terms
        )

        has_continuation = any(
            term in text
            for term in continuation_terms
        )

        has_previous_evidence = bool(
            history
            or research_state.get("sources")
            or research_state.get("current_answer")
        )

        if (
            has_follow_up_evidence
            and has_previous_evidence
            and (
                has_continuation
                or "keterbatasan" in text
                or "kelebihan" in text
                or "kekurangan" in text
            )
        ):
            return True

        metadata_discovery_terms = (
            "apa yang ada",
            "apa saja",
            "penelitian apa",
            "penelitian yang ada",
            "penelitian yang relevan",
            "penelitian relevan",
            "penelitian terkait",
            "literatur terkait",
            "literatur yang relevan",
            "literatur relevan",
            "jurnal terkait",
            "jurnal yang relevan",
            "dokumen yang relevan",
            "dokumen relevan",
            "sumber penelitian",
            "penelitian tersedia",
            "literatur tersedia",
            "yang tersedia",
            "yang relevan",
            "contoh penelitian",
            "ada penelitian",
            "ada jurnal",
            "ada literatur",
            "di repository",
            "dari repository",
            "dalam repository",
            "terdapat di repository",
            "terdapat dalam repository",
            "berdasarkan repository",
        )

        metadata_discovery_only = any(
            term in text
            for term in metadata_discovery_terms
        )

        substantive_evidence_terms = (
            "isi penelitian",
            "isi jurnal",
            "isi dokumen",
            "fulltext",
            "full text",
            "teks lengkap",
            "metode penelitian",
            "metodologi penelitian",
            "hasil penelitian",
            "hasil eksperimen",
            "temuan penelitian",
            "limitations",
            "keterbatasan penelitian",
            "future work",
            "rekomendasi penelitian",
            "discussion",
            "pembahasan penelitian",
            "evidence",
            "bukti",
            "citation",
            "sitasi",
            "kutipan",
            "bandingkan penelitian",
            "bandingkan jurnal",
            "compare penelitian",
            "comparison",
            "research gap",
            "gap penelitian",
            "kesenjangan penelitian",
            "thesis idea",
            "thesis ideas",
            "ide skripsi",
            "ide tesis",
            "ide penelitian",
        )

        if (
            metadata_discovery_only
            and not any(
                term in text
                for term in substantive_evidence_terms
            )
            and not any(
                term in text
                for term in (
                    "berdasarkan repository",
                    "dari repository",
                    "di repository",
                    "dalam repository",
                    "terdapat di repository",
                    "terdapat dalam repository",
                    "berdasarkan dokumen",
                    "dari dokumen",
                    "di dataset",
                )
            )
        ):
            return False

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
            "dalam repository",
            "terdapat di repository",
            "terdapat dalam repository",
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

        idea_request_terms = (
            "thesis idea",
            "thesis ideas",
            "ide skripsi",
            "ide tesis",
            "ide penelitian",
        )

        has_idea_request = any(
            term in text
            for term in idea_request_terms
        )

        if has_idea_request:
            return True

        if any(
            term in text
            for term in evidence_terms
            if term not in idea_request_terms
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
        research_state: dict | None = None,
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

            score = 0

            for term in topic_terms:
                normalized = term.strip().lower()

                if not normalized:
                    continue

                if " " in normalized:
                    if normalized in searchable:
                        score += 1
                    continue

                pattern = (
                    r"(?<!\\w)"
                    + re.escape(normalized)
                    + r"(?!\\w)"
                )

                if re.search(
                    pattern,
                    searchable,
                    flags=re.IGNORECASE,
                ):
                    score += 1

            if score > 0:
                if score < 1:
                    continue

                evidence_text = str(
                    getattr(item, "text", "")
                    or getattr(item, "page_content", "")
                    or getattr(item, "content", "")
                    or getattr(
                        item,
                        "metadata",
                        {},
                    ).get("text", "")
                    or ""
                ).lower()

                priority_terms = (
                    "pengertian",
                    "definisi",
                    "merupakan",
                    "adalah",
                    "penelitian adalah",
                    "penelitian merupakan",
                    "tujuan penelitian",
                    "landasan teori",
                )

                if any(
                    term in evidence_text
                    for term in priority_terms
                ):
                    score += 3

                blocked_terms = (
                    "orientation script",
                    "background questionnaire",
                    "jadwal pengujian",
                    "mempersiapkan bahan pengujian",
                )

                if any(
                    term in evidence_text
                    for term in blocked_terms
                ):
                    score -= 2

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
                -int(item[6]),
                -item[0],
                item[1].lower(),
            )
        )

        unique = []

        seen_documents = set()

        for item in scored:
            document_id = str(item[5])

            if document_id in seen_documents:
                continue

            seen_documents.add(document_id)
            unique.append(item)

        selected = unique[:limit]

        if not selected:
            return ""

        state = research_state

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

        evidence_turn = self._requires_evidence(
            question,
            history,
            research_state,
        )

        if research_turn:
            discovery_topic = (
                research_state.get("topic")
                or research_state.get(
                    "research_direction"
                )
                or ""
            )

            discovery_context = (
                self._build_metadata_discovery_context(
                    discovery_topic,
                    research_state=research_state,
                )
            )

            discovered = list(
                research_state.get(
                    "discovered_documents"
                )
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

            document_ids = []

            if is_continuation and topic:
                rag_query = (
                    f"Research topic: {topic}. "
                    f"Research direction: "
                    f"{research_state.get('research_direction') or topic}. "
                    f"User follow-up: {question}"
                )

                if discovered_documents:
                    document_ids = [
                        str(item.get("document_id", ""))
                        for item in discovered_documents
                        if (
                            item.get("document_id")
                            and item.get("has_pdf") is True
                        )
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

                if topic:
                    rag_query = (
                        f"Research topic: {topic}. "
                        f"Research direction: "
                        f"{research_state.get('research_direction') or topic}. "
                        f"User research request: {question}"
                    )

                if research_gap:
                    rag_query += (
                        f" Existing research gap: {research_gap}"
                    )

                if thesis_idea:
                    rag_query += (
                        f" Existing thesis direction: {thesis_idea}"
                    )

            if not document_ids and discovered_documents:
                document_ids = [
                    str(item.get("document_id", ""))
                    for item in discovered_documents
                    if (
                        item.get("document_id")
                        and item.get("has_pdf") is True
                    )
                ]

            rag = await self.get_rag().build(
                query=rag_query,
                document_ids=(
                    document_ids
                    if document_ids
                    else None
                ),
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

        if discovery_context and not evidence_turn:
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
                    else (
                        "discovery"
                        if discovery_context
                        else "conversation"
                    )
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

        # ANSWER_SYNTHESIS_FALLBACK_766918
        #
        # RAG evidence is already available at this point.
        # The previous fallback could accidentally pass internal prompt
        # fragments back into the repair request. Build a fresh evidence
        # payload directly from the existing messages instead.
        synthesis_answer = generated

        def _answer_needs_synthesis_repair(value):
            if value is None:
                return True

            try:
                normalized = str(value).strip().lower()
            except Exception:
                return True

            if not normalized:
                return True

            bad_patterns = (
                "informasi yang relevan tidak ditemukan",
                "tidak ditemukan dalam context",
                "tidak ditemukan dalam konteks",
                "evidence tidak ditemukan",
                "evidence tidak tersedia",
                "relevant information was not found",
                "not found in the context",
            )

            return any(pattern in normalized for pattern in bad_patterns)

        if _answer_needs_synthesis_repair(synthesis_answer):
            clean_evidence_parts = []

            for message in messages:
                if not isinstance(message, dict):
                    continue

                role = str(message.get("role", "")).strip().lower()
                content = message.get("content")

                if role not in ("system", "user"):
                    continue

                if not isinstance(content, str):
                    continue

                normalized_content = content.strip()

                if not normalized_content:
                    continue

                # Only retain messages that actually contain document
                # evidence. Internal state/prompt instructions are excluded.
                evidence_markers = (
                    "DOCUMENT CONTEXT",
                    "[SOURCE ",
                    "EVIDENCE DOKUMEN",
                    "EVIDENCE DOKUMEN YANG WAJIB DIGUNAKAN",
                )

                if any(
                    marker in normalized_content
                    for marker in evidence_markers
                ):
                    clean_evidence_parts.append(normalized_content)

            clean_evidence = "\n\n".join(clean_evidence_parts).strip()

            if clean_evidence:
                # Prevent accidental prompt explosion while keeping enough
                # evidence for the MVP answer synthesis.
                clean_evidence = clean_evidence[:24000]

                repair_messages = [
                    {
                        "role": "system",
                        "content": (
                            "Anda adalah DELBot, AI Research Assistant akademik.\n\n"
                            "Jawab pertanyaan pengguna hanya berdasarkan evidence "
                            "dokumen yang diberikan.\n\n"
                            "Aturan:\n"
                            "1. Jawab langsung pertanyaan.\n"
                            "2. Gunakan hanya evidence yang tersedia.\n"
                            "3. Sintesis evidence dengan kata-kata sendiri.\n"
                            "4. Jangan menyalin context mentah.\n"
                            "5. Jangan menyebut context, prompt, atau instruksi internal.\n"
                            "6. Jangan mengarang fakta.\n"
                            "7. Jika evidence memang tidak cukup, nyatakan keterbatasannya.\n"
                            "8. Jika evidence cukup, jangan mengatakan informasi tidak ditemukan.\n"
                            "9. Untuk pertanyaan sederhana, jawab 1-3 paragraf pendek.\n"
                            "10. Output hanya jawaban final."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "PERTANYAAN PENGGUNA:\n"
                            f"{question}\n\n"
                            "EVIDENCE DOKUMEN:\n"
                            f"{clean_evidence}\n\n"
                            "JAWAB SEKARANG."
                        ),
                    },
                ]

                try:
                    repaired = self.generator.generate(
                        repair_messages,
                    )

                    if inspect.isawaitable(repaired):
                        repaired = await repaired

                    if not _answer_needs_synthesis_repair(repaired):
                        synthesis_answer = repaired
                except Exception:
                    synthesis_answer = generated

        research_state["current_answer"] = synthesis_answer


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

        return ResearchPipelineResponse(
            answer=generated,
            citations=citations,
            research_state=research_state,
            rag=rag,
        )
