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



    def _build_metadata_complement_context(
        self,
        query: str,
        limit: int = 3,
        research_state: dict | None = None,
    ) -> str:
        """Select relevant metadata-only abstracts."""

        # BROAD_METADATA_COMPLEMENT_767797
        import json as _json
        import re as _re
        from pathlib import Path as _Path

        normalized_query = _re.sub(
            r"[^a-z0-9]+",
            " ",
            str(query or "").lower(),
        ).strip()

        stopwords = {
            "yang",
            "dan",
            "dari",
            "dalam",
            "untuk",
            "dengan",
            "pada",
            "atau",
            "oleh",
            "ini",
            "itu",
            "beberapa",
            "tentang",
            "berdasarkan",
            "jelaskan",
            "digunakan",
            "diharapkan",
            "penelitian",
            "research",
            "thesis",
            "ideas",
            "idea",
            "sumber",
            "evidence",
            "koleksi",
            "repositori",
            "the",
            "and",
            "for",
            "from",
            "using",
            "study",
        }

        query_terms = {
            term
            for term in normalized_query.split()
            if len(term) >= 3
            and term not in stopwords
        }

        expanded_terms = set(query_terms)

        if (
            "iot" in query_terms
            or "internet" in query_terms
        ):
            expanded_terms.update({
                "iot",
                "internet",
                "things",
                "sensor",
                "monitoring",
                "esp32",
                "nodemcu",
                "mqtt",
                "lora",
                "otomasi",
            })

        agriculture_terms = {
            "pertanian",
            "agriculture",
            "agricultural",
            "tanaman",
            "tanah",
            "hidroponik",
            "irigasi",
            "soil",
            "crop",
        }

        if query_terms.intersection(
            agriculture_terms
        ):
            expanded_terms.update({
                "pertanian",
                "agriculture",
                "agricultural",
                "tanaman",
                "tanah",
                "hidroponik",
                "irigasi",
                "kelembaban",
                "cuaca",
                "soil",
                "crop",
                "nutrisi",
            })

        catalog_paths = [
            (
                _Path(__file__).resolve().parents[2]
                / "repository_data/metadata/"
                "repository_catalog.json"
            ),
            (
                _Path.cwd()
                / "delbot_platform/repository_data/"
                "metadata/repository_catalog.json"
            ),
        ]

        records = []

        for catalog_path in catalog_paths:
            if not catalog_path.is_file():
                continue

            try:
                catalog_data = _json.loads(
                    catalog_path.read_text(
                        encoding="utf-8",
                        errors="replace",
                    )
                )
            except Exception:
                continue

            if isinstance(catalog_data, list):
                records = catalog_data
            elif isinstance(catalog_data, dict):
                for key in (
                    "items",
                    "documents",
                    "records",
                    "data",
                ):
                    value = catalog_data.get(key)

                    if isinstance(value, list):
                        records = value
                        break

            if records:
                break

        ranked_documents = []

        for record in records:
            if not isinstance(record, dict):
                continue

            nested = record.get("metadata")

            if not isinstance(nested, dict):
                nested = {}

            document_id = str(
                record.get("document_id")
                or record.get("id")
                or nested.get("document_id")
                or ""
            ).strip()

            title = str(
                record.get("title")
                or nested.get("title")
                or ""
            ).strip()

            abstract = str(
                record.get("abstract")
                or nested.get("abstract")
                or ""
            ).strip()

            author = (
                record.get("author")
                or nested.get("author")
                or ""
            )

            year = (
                record.get("year")
                or nested.get("year")
                or ""
            )

            has_pdf_value = record.get(
                "has_pdf"
            )

            if has_pdf_value is None:
                has_pdf_value = nested.get(
                    "has_pdf"
                )

            pdf_path = str(
                record.get("pdf_path")
                or nested.get("pdf_path")
                or ""
            ).strip()

            if isinstance(has_pdf_value, str):
                has_pdf = (
                    has_pdf_value.strip().lower()
                    in ("1", "true", "yes")
                )
            elif has_pdf_value is None:
                has_pdf = bool(pdf_path)
            else:
                has_pdf = bool(has_pdf_value)

            if has_pdf or not abstract:
                continue

            normalized_title = _re.sub(
                r"[^a-z0-9]+",
                " ",
                title.lower(),
            )

            normalized_abstract = _re.sub(
                r"[^a-z0-9]+",
                " ",
                abstract.lower(),
            )

            title_terms = set(
                normalized_title.split()
            )
            abstract_terms = set(
                normalized_abstract.split()
            )

            title_matches = len(
                expanded_terms.intersection(
                    title_terms
                )
            )

            abstract_matches = len(
                expanded_terms.intersection(
                    abstract_terms
                )
            )

            score = (
                title_matches * 6
                + abstract_matches
            )

            if (
                "iot" in normalized_title
                or "internet of things"
                in normalized_abstract
            ):
                score += 8

            if any(
                term in normalized_title
                or term in normalized_abstract
                for term in (
                    "pertanian",
                    "tanaman",
                    "tanah",
                    "hidroponik",
                    "irigasi",
                    "soil",
                    "agriculture",
                )
            ):
                score += 8

            if score <= 0:
                continue

            ranked_documents.append({
                "score": score,
                "document_id": document_id,
                "title": title,
                "abstract": abstract,
                "author": author,
                "year": year,
                "has_pdf": False,
                "evidence_type": (
                    "metadata_abstract"
                ),
            })

        ranked_documents.sort(
            key=lambda item: (
                -item["score"],
                item["title"],
            )
        )

        selected = ranked_documents[
            :max(1, int(limit))
        ]

        if not selected:
            return ""

        if research_state is not None:
            research_state[
                "metadata_complements"
            ] = selected

        context_parts = [
            "METADATA ABSTRACT COMPLEMENT",
            (
                "The following metadata-only abstracts "
                "complement the primary fulltext "
                "evidence. They are not PDF page "
                "evidence."
            ),
        ]

        for index, document in enumerate(
            selected,
            start=1,
        ):
            context_parts.extend([
                "",
                f"[Metadata Complement {index}]",
                (
                    "Document ID: "
                    + document["document_id"]
                ),
                "Title: " + document["title"],
                (
                    "Author: "
                    + str(document["author"])
                ),
                (
                    "Year: "
                    + str(document["year"])
                ),
                "Has PDF: False",
                (
                    "Evidence Type: "
                    "metadata_abstract"
                ),
                (
                    "Abstract: "
                    + document["abstract"][:1800]
                ),
            ])

        return "\n".join(context_parts)


    def _build_exact_metadata_context(
        self,
        query: str,
        research_state: dict | None = None,
    ) -> str:
        """Resolve an explicitly named metadata-only record."""

        # EXACT_METADATA_IDENTIFIER_LOOKUP_767793
        import json as _json
        import re as _re
        from pathlib import Path as _Path

        normalized_query = _re.sub(
            r"[^a-z0-9]+",
            " ",
            str(query or "").lower(),
        ).strip()

        requested_ids = set(
            _re.findall(
                r"\b\d{6,}-\d+\b",
                str(query or ""),
            )
        )

        catalog_paths = [
            (
                _Path(__file__).resolve().parents[2]
                / "repository_data/metadata/"
                "repository_catalog.json"
            ),
            (
                _Path.cwd()
                / "delbot_platform/repository_data/"
                "metadata/repository_catalog.json"
            ),
        ]

        catalog_records = []

        for catalog_path in catalog_paths:
            if not catalog_path.is_file():
                continue

            try:
                catalog_data = _json.loads(
                    catalog_path.read_text(
                        encoding="utf-8",
                        errors="replace",
                    )
                )
            except Exception:
                continue

            if isinstance(catalog_data, list):
                catalog_records = catalog_data
            elif isinstance(catalog_data, dict):
                for collection_key in (
                    "items",
                    "documents",
                    "records",
                    "data",
                ):
                    collection_value = (
                        catalog_data.get(collection_key)
                    )

                    if isinstance(
                        collection_value,
                        list,
                    ):
                        catalog_records = (
                            collection_value
                        )
                        break

            if catalog_records:
                break

        exact_documents = []

        for record in catalog_records:
            if not isinstance(record, dict):
                continue

            nested_metadata = record.get(
                "metadata"
            )

            if not isinstance(
                nested_metadata,
                dict,
            ):
                nested_metadata = {}

            document_id = str(
                record.get("document_id")
                or record.get("id")
                or nested_metadata.get("document_id")
                or ""
            ).strip()

            title = str(
                record.get("title")
                or nested_metadata.get("title")
                or ""
            ).strip()

            abstract = str(
                record.get("abstract")
                or nested_metadata.get("abstract")
                or ""
            ).strip()

            author = record.get("author")

            if author in (None, ""):
                author = nested_metadata.get(
                    "author",
                    "",
                )

            year = record.get("year")

            if year in (None, ""):
                year = nested_metadata.get(
                    "year",
                    "",
                )

            has_pdf_value = record.get(
                "has_pdf"
            )

            if has_pdf_value is None:
                has_pdf_value = nested_metadata.get(
                    "has_pdf"
                )

            pdf_path = str(
                record.get("pdf_path")
                or record.get("file_path")
                or nested_metadata.get("pdf_path")
                or nested_metadata.get("file_path")
                or ""
            ).strip()

            if isinstance(has_pdf_value, str):
                has_pdf = (
                    has_pdf_value.strip().lower()
                    in ("1", "true", "yes")
                )
            elif has_pdf_value is None:
                has_pdf = bool(pdf_path)
            else:
                has_pdf = bool(has_pdf_value)

            normalized_title = _re.sub(
                r"[^a-z0-9]+",
                " ",
                title.lower(),
            ).strip()

            identifier_match = (
                bool(document_id)
                and document_id in requested_ids
            )

            title_match = (
                len(normalized_title) >= 18
                and normalized_title
                in normalized_query
            )

            if not (
                identifier_match
                or title_match
            ):
                continue

            if has_pdf:
                continue

            if not abstract:
                continue

            exact_documents.append({
                "document_id": document_id,
                "title": title,
                "abstract": abstract,
                "author": author,
                "year": year,
                "has_pdf": False,
                "evidence_type": (
                    "metadata_abstract"
                ),
            })

            if identifier_match:
                break

        if not exact_documents:
            return ""

        if research_state is not None:
            previous_documents = list(
                research_state.get(
                    "discovered_documents"
                )
                or []
            )

            exact_ids = {
                document.get("document_id")
                for document in exact_documents
            }

            research_state[
                "discovered_documents"
            ] = (
                exact_documents
                + [
                    document
                    for document
                    in previous_documents
                    if not isinstance(document, dict)
                    or document.get("document_id")
                    not in exact_ids
                ]
            )

            research_state[
                "discovery_topic"
            ] = query

        context_parts = [
            "EXACT METADATA EVIDENCE",
            (
                "The records below are metadata or "
                "abstract evidence because PDF fulltext "
                "is unavailable."
            ),
            (
                "Do not claim a PDF page, section, or "
                "fulltext statement from this evidence."
            ),
        ]

        for index, document in enumerate(
            exact_documents,
            start=1,
        ):
            context_parts.extend([
                "",
                f"[Metadata Source {index}]",
                (
                    "Document ID: "
                    + document["document_id"]
                ),
                "Title: " + document["title"],
                (
                    "Author: "
                    + str(document["author"])
                ),
                (
                    "Year: "
                    + str(document["year"])
                ),
                "Has PDF: False",
                (
                    "Evidence Type: "
                    "metadata_abstract"
                ),
                (
                    "Abstract: "
                    + document["abstract"][:4000]
                ),
            ])

        return "\n".join(context_parts)


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


        # EXACT_METADATA_OVERRIDE_767793
        #
        # Fulltext remains primary for ordinary retrieval.
        # An explicitly named metadata-only document must
        # replace unrelated Qdrant results.
        exact_metadata_state = {}

        exact_metadata_context = (
            self._build_exact_metadata_context(
                question,
                research_state=exact_metadata_state,
            )
        )

        exact_metadata_documents = list(
            exact_metadata_state.get(
                "discovered_documents"
            )
            or []
        )

        if (
            exact_metadata_context
            and exact_metadata_documents
        ):
            context = exact_metadata_context
            metadata_citations = []

            for metadata_document in (
                exact_metadata_documents
            ):
                if not isinstance(
                    metadata_document,
                    dict,
                ):
                    continue

                document_id = str(
                    metadata_document.get(
                        "document_id"
                    )
                    or ""
                ).strip()

                title = str(
                    metadata_document.get("title")
                    or ""
                ).strip()

                abstract = str(
                    metadata_document.get(
                        "abstract"
                    )
                    or ""
                ).strip()

                author = metadata_document.get(
                    "author"
                )

                if isinstance(author, list):
                    author_names = [
                        str(value)
                        for value in author
                        if value
                    ]
                elif author:
                    author_names = [str(author)]
                else:
                    author_names = []

                metadata_citations.append({
                    "document": {
                        "document_id": document_id,
                        "title": title,
                        "file_path": "",
                        "authors": [
                            {
                                "author_id": "",
                                "full_name": name,
                                "email": "",
                                "orcid": "",
                                "metadata": {},
                            }
                            for name in author_names
                        ],
                        "entities": [],
                        "metadata": {
                            "has_pdf": False,
                            "metadata_only": True,
                            "evidence_type": (
                                "metadata_abstract"
                            ),
                        },
                    },
                    "page": None,
                    "chunk_id": (
                        "metadata:" + document_id
                    ),
                    "score": 1.0,
                    "text": abstract,
                    "metadata": {
                        "page_start": None,
                        "page_end": None,
                        "section": "",
                        "has_pdf": False,
                        "metadata_only": True,
                        "evidence_type": (
                            "metadata_abstract"
                        ),
                    },
                })

            citations = metadata_citations

            research_state[
                "discovered_documents"
            ] = exact_metadata_documents

            research_state["sources"] = list(
                metadata_citations
            )

        else:
            complement_state = {}

            metadata_complement_context = (
                self._build_metadata_complement_context(
                    question,
                    limit=3,
                    research_state=complement_state,
                )
            )

            metadata_complements = list(
                complement_state.get(
                    "metadata_complements"
                )
                or []
            )

            if metadata_complement_context:
                if context:
                    context = (
                        context
                        + "\n\n"
                        + metadata_complement_context
                    )
                else:
                    context = (
                        metadata_complement_context
                    )

                metadata_citations = []

                for item in metadata_complements:
                    if not isinstance(item, dict):
                        continue

                    document_id = str(
                        item.get("document_id")
                        or ""
                    ).strip()

                    title = str(
                        item.get("title")
                        or ""
                    ).strip()

                    abstract = str(
                        item.get("abstract")
                        or ""
                    ).strip()

                    author = item.get("author")

                    if isinstance(author, list):
                        author_names = [
                            str(value)
                            for value in author
                            if value
                        ]
                    elif author:
                        author_names = [
                            str(author)
                        ]
                    else:
                        author_names = []

                    metadata_citations.append({
                        "document": {
                            "document_id": (
                                document_id
                            ),
                            "title": title,
                            "file_path": "",
                            "authors": [
                                {
                                    "author_id": "",
                                    "full_name": name,
                                    "email": "",
                                    "orcid": "",
                                    "metadata": {},
                                }
                                for name
                                in author_names
                            ],
                            "entities": [],
                            "metadata": {
                                "has_pdf": False,
                                "metadata_only": True,
                                "evidence_type": (
                                    "metadata_abstract"
                                ),
                            },
                        },
                        "page": None,
                        "chunk_id": (
                            "metadata:"
                            + document_id
                        ),
                        "score": float(
                            item.get("score")
                            or 0.0
                        ),
                        "text": abstract,
                        "metadata": {
                            "page_start": None,
                            "page_end": None,
                            "section": "",
                            "has_pdf": False,
                            "metadata_only": True,
                            "evidence_type": (
                                "metadata_abstract"
                            ),
                        },
                    })

                citations.extend(
                    metadata_citations
                )

                research_state[
                    "metadata_complements"
                ] = metadata_complements

                persisted_sources = list(
                    research_state.get(
                        "sources"
                    )
                    or []
                )

                persisted_sources.extend(
                    metadata_citations
                )

                research_state["sources"] = (
                    persisted_sources[-20:]
                )

            elif discovery_context and not context:
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
                # GROUNDED_THESIS_REPAIR_767799
                "3. Untuk permintaan thesis ideas, jika context memuat evidence relevan, jangan mengembalikan refusal menyeluruh.\n"
                "4. Hasilkan tepat tiga ide grounded dengan heading Ide 1, Ide 2, dan Ide 3.\n"
                "5. Setiap ide harus memuat masalah, gap, metode usulan, evaluasi usulan, kontribusi usulan, keterbatasan, dan sumber pendukung.\n"
                "6. Bedakan fakta dari evidence dengan proposal atau inference yang belum diuji.\n"
                "7. Keterbatasan metadata atau fulltext harus dijelaskan, tetapi tidak boleh menghapus ide yang masih dapat diturunkan secara sah dari evidence.\n"
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
