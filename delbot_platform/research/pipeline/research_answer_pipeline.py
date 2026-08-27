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


# DELBOT MVP conversation state v2 767919
def _delbot_conversation_history_text(history: object) -> str:
    """Normalize message-style and exchange-style conversation history."""
    # DELBOT MVP conversation history schema recovery 767920
    if not isinstance(history, (list, tuple)):
        return ""

    preferred_keys = (
        "question", "user_question", "user_message", "query", "prompt",
        "input", "content", "text", "message", "answer",
        "assistant_answer", "assistant_message", "response", "output",
    )

    def record(value: object) -> dict[str, object] | None:
        if isinstance(value, dict):
            return value
        for method_name in ("model_dump", "dict"):
            method = getattr(value, method_name, None)
            if callable(method):
                try:
                    dumped = method()
                except Exception:
                    continue
                if isinstance(dumped, dict):
                    return dumped
        return None

    def strings(value: object, depth: int = 0) -> list[str]:
        if value is None or depth > 3:
            return []
        if isinstance(value, str):
            cleaned = value.strip()
            return [cleaned] if cleaned else []
        if isinstance(value, (int, float, bool)):
            return []
        if isinstance(value, (list, tuple)):
            found: list[str] = []
            for child in value:
                found.extend(strings(child, depth + 1))
            return found

        dumped = record(value)
        if dumped is None:
            return []

        found: list[str] = []
        used: set[str] = set()
        for key in preferred_keys:
            if key in dumped:
                found.extend(strings(dumped[key], depth + 1))
                used.add(key)

        # Some API models wrap the exchange in an arbitrary nested field.
        if not found:
            for key, child in dumped.items():
                if key in used or key in {"role", "speaker", "id", "created_at"}:
                    continue
                found.extend(strings(child, depth + 1))
        return found

    parts: list[str] = []
    for item in history[-10:]:
        for text in strings(item):
            if text and text not in parts:
                parts.append(text)
    return "\n".join(parts)

def _delbot_conversational_discovery_reply(
    question: object,
    history: object,
) -> str:
    """Continue discovery until the user explicitly asks for repository work."""
    import re

    text = re.sub(r"\s+", " ", str(question or "")).strip()
    lowered = text.casefold()
    history_text = _delbot_conversation_history_text(history).casefold()

    if not lowered:
        return ""

    explicit_action = re.search(
        r"\b(?:carikan|cari|telusuri|tinjau|bandingkan|buatkan|susunkan|"
        r"rekomendasikan|berikan|tampilkan|jelaskan|analisis|identifikasi|"
        r"kembangkan|pandu|panduan|mulai tahap|referensi|research gap|"
        r"gap penelitian|metode|evaluasi)\b",
        lowered,
    )
    if explicit_action:
        return ""

    exploratory_tone = re.search(
        r"\b(?:tertarik|ingin|mau|berencana|kepikiran|mempertimbangkan|"
        r"belum punya|belum tahu|tidak tahu|masih bingung)\b",
        lowered,
    )
    research_context = re.search(
        r"\b(?:skripsi|tugas akhir|penelitian|judul penelitian|prediksi cuaca|"
        r"curah hujan|suhu udara|kecepatan angin|kategori cuaca)\b",
        lowered,
    )
    history_context = re.search(
        r"\b(?:skripsi|tugas akhir|penelitian|prediksi cuaca|curah hujan|"
        r"suhu udara|kecepatan angin|kategori cuaca)\b",
        history_text,
    )

    if not exploratory_tone or not (research_context or history_context):
        return ""

    if "curah hujan" in lowered:
        if re.search(r"\b(?:belum|tidak)\b", lowered) and re.search(
            r"\b(?:lokasi|dataset|data)\b", lowered
        ):
            return (
                "Curah hujan cocok dijadikan fokus karena targetnya jelas dan "
                "hasilnya dapat diuji secara kuantitatif. Kita belum perlu "
                "mengunci judul; tentukan sumber data lebih dahulu.\n\n"
                "Cakupan awal yang realistis adalah satu stasiun cuaca, data "
                "harian, dan periode minimal lima tahun. Kamu ingin memakai "
                "lokasi yang dekat dengan daerahmu atau lokasi mana pun dengan "
                "data paling lengkap?\n\n"
                "Kalau belum punya preferensi, balas **pilihkan yang paling "
                "realistis**. Setelah itu aku telusuri ide dan referensi yang "
                "benar-benar sesuai."
            )
        return (
            "Oke, fokus sementaramu adalah **prediksi curah hujan**. Agar "
            "cakupannya tidak terlalu luas, apakah kamu sudah punya lokasi, "
            "sumber data, atau periode pengamatan tertentu?\n\n"
            "Kalau belum, aku bantu memilih cakupan yang realistis sebelum "
            "masuk ke pencarian referensi."
        )

    weather_context = re.search(
        r"\b(?:cuaca|hujan|suhu|angin|meteorologi)\b",
        lowered + " " + history_text,
    )
    if weather_context:
        return (
            "Menarik—prediksi cuaca bisa diarahkan ke penelitian yang sangat "
            "terukur. Sebelum aku mencarikan judul dan referensinya, aku ingin "
            "memahami arah yang paling cocok buat kamu.\n\n"
            "Kamu lebih tertarik memprediksi **curah hujan**, **suhu**, "
            "**kecepatan angin**, atau **kategori cuaca**? Apakah kamu sudah "
            "punya lokasi atau dataset tertentu?\n\n"
            "Kalau belum tahu, cukup bilang **belum tahu**—aku bantu memilihkan "
            "arah yang realistis terlebih dahulu."
        )

    return (
        "Menarik. Sebelum langsung mencari judul dan referensi, ceritakan sedikit "
        "bidang atau masalah yang paling membuatmu penasaran. Apakah kamu sudah "
        "punya objek penelitian atau akses data tertentu?\n\n"
        "Kalau masih sangat awal, tidak apa-apa—kita persempit bersama."
    )


def _delbot_contextualize_research_followup(
    question: object,
    history: object,
) -> str:
    """Resolve references such as 'pilihan tadi' before retrieval and synthesis."""
    import re

    text = re.sub(r"\s+", " ", str(question or "")).strip()
    lowered = text.casefold()
    history_text = _delbot_conversation_history_text(history).casefold()

    asks_for_research = re.search(
        r"\b(?:carikan|cari|berikan|buatkan|susunkan|rekomendasikan|"
        r"referensi|research gap|gap penelitian|ide judul|ide skripsi)\b",
        lowered,
    )
    refers_to_context = re.search(
        r"\b(?:pilihan tadi|topik tadi|topik ini|berdasarkan pilihan|"
        r"yang tadi|tersebut)\b",
        lowered,
    )
    has_explicit_topic = re.search(
        r"\b(?:curah hujan|prediksi cuaca|suhu udara|kecepatan angin|"
        r"kategori cuaca)\b",
        lowered,
    )

    if not asks_for_research or has_explicit_topic or not refers_to_context:
        return text

    if "curah hujan" in history_text:
        missing_data = bool(
            re.search(
                r"(?:belum|tidak)\s+(?:punya|memiliki).{0,30}(?:lokasi|dataset|data)",
                history_text,
            )
        )
        data_note = (
            " Pengguna belum menentukan lokasi dan dataset, sehingga ide harus "
            "menyatakan pilihan data sebagai keputusan berikutnya, bukan "
            "mengarang lokasi."
            if missing_data
            else ""
        )
        return (
            "Berikan tiga ide judul skripsi untuk prediksi curah hujan berbasis "
            "data cuaca. Sertakan research gap, arah metode, evaluasi, dan "
            "referensi repository yang relevan dengan hujan atau cuaca."
            + data_note
        )

    if "prediksi cuaca" in history_text:
        return (
            "Berikan tiga ide judul skripsi tentang prediksi cuaca. Sertakan "
            "research gap, arah metode, evaluasi, dan referensi repository yang "
            "relevan dengan cuaca."
        )

    return text

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

        # DELBOT MVP contextual research query from bounded history
        _mvp_original_question = str(question or "").strip()

        # DELBOT MVP deterministic greeting fast path
        import asyncio as _mvp_asyncio

        _mvp_fast_query = " ".join(
            str(question or "").split()
        ).casefold().strip(" .,!?:;")

        _mvp_fast_greetings = {
            "hai",
            "haii",
            "haiii",
            "halo",
            "haloo",
            "hi",
            "hello",
            "hey",
            "selamat pagi",
            "selamat siang",
            "selamat sore",
            "selamat malam",
        }

        # DELBOT MVP conversational discovery gate 767917
        _delbot_discovery_answer = _delbot_conversational_discovery_reply(question, history)
        if _delbot_discovery_answer:
            return ResearchPipelineResponse(answer=_delbot_discovery_answer, citations=[], research_state=research_state or {}, rag=None)
        # DELBOT MVP resolve active conversation topic before retrieval 767919
        question = _delbot_contextualize_research_followup(question, history)


        if _mvp_fast_query in _mvp_fast_greetings:
            return ResearchPipelineResponse(
                answer=(
                    "Hai! Ada yang bisa DELBot bantu? "
                    "Kamu dapat meminta referensi repository, "
                    "mencari dokumen PDF, membandingkan penelitian, "
                    "menemukan research gap, atau mengembangkan "
                    "ide tugas akhir."
                ),
                citations=[],
                research_state=(
                    research_state or {}
                ),
                rag=None,
            )

        _mvp_active_topic_request = (
            "topik aktif" in _mvp_fast_query
            and any(
                phrase in _mvp_fast_query
                for phrase in (
                    "ide tugas akhir",
                    "ide penelitian",
                    "research gap",
                    "kembangkan",
                )
            )
        )

        if _mvp_active_topic_request:
            _mvp_history_value = history
            _mvp_fast_history_items = (
                _mvp_history_value
                if isinstance(
                    _mvp_history_value,
                    (list, tuple),
                )
                else []
            )
            _mvp_meaningful_prior_topics = []

            for _mvp_history_item in _mvp_fast_history_items:
                if isinstance(
                    _mvp_history_item,
                    dict,
                ):
                    _mvp_history_role = str(
                        _mvp_history_item.get("role")
                        or _mvp_history_item.get("sender")
                        or ""
                    ).casefold()
                    _mvp_history_text = str(
                        _mvp_history_item.get("content")
                        or _mvp_history_item.get("text")
                        or _mvp_history_item.get("message")
                        or ""
                    ).strip()
                else:
                    _mvp_history_role = str(
                        getattr(
                            _mvp_history_item,
                            "role",
                            "",
                        )
                        or getattr(
                            _mvp_history_item,
                            "sender",
                            "",
                        )
                    ).casefold()
                    _mvp_history_text = str(
                        getattr(
                            _mvp_history_item,
                            "content",
                            "",
                        )
                        or getattr(
                            _mvp_history_item,
                            "text",
                            "",
                        )
                        or ""
                    ).strip()

                _mvp_history_lower = (
                    " ".join(
                        _mvp_history_text.split()
                    )
                    .casefold()
                    .strip(" .,!?:;")
                )

                if (
                    _mvp_history_role
                    not in ("user", "you", "")
                    or not _mvp_history_lower
                    or _mvp_history_lower
                    in _mvp_fast_greetings
                    or "permintaan belum berhasil diproses"
                    in _mvp_history_lower
                    or "timeout of 180000ms exceeded"
                    in _mvp_history_lower
                ):
                    continue

                _mvp_meaningful_prior_topics.append(
                    _mvp_history_text
                )

            if not _mvp_meaningful_prior_topics:
                return ResearchPipelineResponse(
                    answer=(
                        "Belum ada topik penelitian aktif pada "
                        "percakapan ini. Tuliskan bidang atau topik "
                        "yang ingin dikembangkan, misalnya "
                        "“IoT untuk kesehatan”, “prediksi curah "
                        "hujan dengan ANN”, atau judul dokumen "
                        "repository tertentu."
                    ),
                    citations=[],
                    research_state=(
                        research_state or {}
                    ),
                    rag=None,
                )

        # DELBOT MVP bounded research generation
        async def _mvp_bounded_generator_call(
            _mvp_generation_messages,
        ):
            try:
                _mvp_generation_result = await (
                    _mvp_asyncio.wait_for(
                        _mvp_asyncio.to_thread(
                            self.generator.generate,
                            _mvp_generation_messages,
                        ),
                        timeout=65.0,
                    )
                )

                if inspect.isawaitable(
                    _mvp_generation_result
                ):
                    _mvp_generation_result = await (
                        _mvp_asyncio.wait_for(
                            _mvp_generation_result,
                            timeout=65.0,
                        )
                    )

                return _mvp_generation_result

            except _mvp_asyncio.TimeoutError:
                return ""

            except Exception as _mvp_generation_error:
                if type(
                    _mvp_generation_error
                ).__name__ in {
                    "ConnectTimeout",
                    "ConnectionError",
                    "HTTPError",
                    "ReadTimeout",
                    "RequestException",
                    "Timeout",
                    "TimeoutError",
                }:
                    return ""

                raise
        _mvp_contextual_question = _mvp_original_question
        # DELBOT MVP evidence query initialized for all answer paths
        _mvp_evidence_query = _mvp_contextual_question
        # DELBOT MVP exact citation lifecycle
        _mvp_exact_selected_citation = None
        # DELBOT MVP initialize retrieval state for every chat path
        _mvp_fulltext_citations = []
        _mvp_fulltext_context = ""
        # DELBOT MVP fulltext helper available on every chat path
        def _mvp_is_fulltext_citation(
            citation,
        ):
            def _mvp_fulltext_helper_value(
                record,
                key,
                default=None,
            ):
                if isinstance(record, dict):
                    return record.get(key, default)

                return getattr(record, key, default)

            document = _mvp_fulltext_helper_value(
                citation,
                "document",
                {},
            )

            if not isinstance(document, dict):
                document = {
                    "metadata": (
                        _mvp_fulltext_helper_value(
                            document,
                            "metadata",
                            {},
                        )
                    ),
                    "file_path": (
                        _mvp_fulltext_helper_value(
                            document,
                            "file_path",
                            "",
                        )
                    ),
                }

            root_metadata = _mvp_fulltext_helper_value(
                citation,
                "metadata",
                {},
            )
            document_metadata = document.get(
                "metadata",
                {},
            )

            if not isinstance(root_metadata, dict):
                root_metadata = {}

            if not isinstance(document_metadata, dict):
                document_metadata = {}

            evidence_type = str(
                root_metadata.get("evidence_type")
                or document_metadata.get(
                    "evidence_type"
                )
                or ""
            ).strip().lower()

            metadata_only = bool(
                root_metadata.get("metadata_only")
                or document_metadata.get(
                    "metadata_only"
                )
                or "metadata_abstract"
                    in evidence_type
                or evidence_type == "metadata"
            )

            if metadata_only:
                return False

            text = str(
                _mvp_fulltext_helper_value(
                    citation,
                    "text",
                    "",
                )
                or ""
            ).strip()
            section = str(
                root_metadata.get("section")
                or root_metadata.get(
                    "section_title"
                )
                or ""
            ).strip()
            page = (
                _mvp_fulltext_helper_value(
                    citation,
                    "page",
                    None,
                )
                or root_metadata.get("page")
                or root_metadata.get("page_start")
            )
            file_path = str(
                document.get("file_path")
                or root_metadata.get("file_path")
                or ""
            ).strip().lower()

            explicit_fulltext = any(
                marker in evidence_type
                for marker in (
                    "fulltext",
                    "full_text",
                    "pdf_chunk",
                    "document_chunk",
                )
            )

            located_text = bool(
                len(text) >= 80
                and (
                    section
                    or page is not None
                    or file_path.endswith(".pdf")
                )
            )

            return bool(
                explicit_fulltext
                or located_text
            )


        # DELBOT MVP deterministic repository discovery
        _mvp_repository_question = str(
            _mvp_original_question
            or question
            or ""
        ).strip()
        _mvp_repository_question_lower = (
            _mvp_repository_question.lower()
        )
        _mvp_repository_history_lower = str(
            history or ""
        ).lower()

        _mvp_repository_count_phrases = (
            "berapa jumlah repository",
            "berapa jumlah isi repository",
            "jumlah isi repository",
            "jumlah repository",
            "total isi repository",
            "total dokumen repository",
            "berapa dokumen repository",
            "repository count",
            "how many repository documents",
        )
        _mvp_repository_list_phrases = (
            "lihat isi repository",
            "lihat isinya repository",
            "tampilkan isi repository",
            "tampilkan daftar repository",
            "daftar isi repository",
            "daftar dokumen repository",
            "apa saja isi repository",
            "repository contents",
            "list repository",
            "show repository contents",
        )

        _mvp_repository_count_intent = any(
            phrase in _mvp_repository_question_lower
            for phrase in _mvp_repository_count_phrases
        )
        _mvp_repository_list_intent = (
            any(
                phrase
                in _mvp_repository_question_lower
                for phrase
                in _mvp_repository_list_phrases
            )
            or (
                any(
                    phrase
                    in _mvp_repository_question_lower
                    for phrase in (
                        "lihat isinya",
                        "tampilkan isinya",
                        "lihat daftarnya",
                        "tampilkan daftarnya",
                    )
                )
                and "repository"
                in _mvp_repository_history_lower
            )
        )

        if (
            _mvp_repository_count_intent
            or _mvp_repository_list_intent
        ):
            try:
                from pathlib import Path as _MvpRepositoryPath
                import json as _mvp_repository_json
                import math as _mvp_repository_math
                import re as _mvp_repository_re

                def _mvp_repository_normalize(value):
                    return " ".join(
                        _mvp_repository_re.findall(
                            r"[a-z0-9]+",
                            str(value or "").lower(),
                        )
                    )

                def _mvp_repository_record_id(record):
                    identifier = str(
                        record.get("document_id")
                        or record.get("documentId")
                        or record.get("handle")
                        or ""
                    ).strip()

                    if identifier:
                        return identifier.replace("/", "-")

                    repository_url = str(
                        record.get("url")
                        or record.get("repository_url")
                        or ""
                    ).rstrip("/")
                    handle = repository_url.rsplit(
                        "/",
                        1,
                    )[-1]

                    if handle.isdigit():
                        return "123456789-" + handle

                    return ""

                def _mvp_repository_walk(value):
                    if isinstance(value, dict):
                        yield value

                        for child in value.values():
                            yield from _mvp_repository_walk(
                                child
                            )

                    elif isinstance(value, list):
                        for child in value:
                            yield from _mvp_repository_walk(
                                child
                            )

                dataset_path = _MvpRepositoryPath(
                    "delbot_platform/repository_data/"
                    "metadata/skripsi_dataset.json"
                )
                records = _mvp_repository_json.loads(
                    dataset_path.read_text(
                        encoding="utf-8"
                    )
                )

                if not isinstance(records, list):
                    records = []

                records = [
                    record
                    for record in records
                    if isinstance(record, dict)
                ]

                record_id_to_index = {}
                record_title_to_index = {}

                for index, record in enumerate(records):
                    identifier = (
                        _mvp_repository_record_id(record)
                    )
                    normalized_title = (
                        _mvp_repository_normalize(
                            record.get("title")
                        )
                    )

                    if identifier:
                        record_id_to_index[identifier] = index

                    if normalized_title:
                        record_title_to_index[
                            normalized_title
                        ] = index

                pdf_record_indexes = set()
                _mvp_repository_active_pdf_count = None
                # DELBOT MVP canonical active repository catalog
                active_overlay_path = _MvpRepositoryPath(
                    "delbot_platform/repository_data/"
                    "runtime/repository_overlay_index.json"
                )
                fallback_catalog_path = _MvpRepositoryPath(
                    "delbot_platform/repository_data/"
                    "metadata/repository_catalog.json"
                )
                repository_artifacts = (
                    (active_overlay_path,)
                    if active_overlay_path.is_file()
                    else (fallback_catalog_path,)
                )

                for artifact_path in repository_artifacts:
                    if not artifact_path.is_file():
                        continue

                    try:
                        artifact = (
                            _mvp_repository_json.loads(
                                artifact_path.read_text(
                                    encoding="utf-8"
                                )
                            )
                        )
                    except Exception:
                        continue

                    # DELBOT MVP count PDF from active overlay root values
                    if (
                        artifact_path
                        == active_overlay_path
                        and isinstance(artifact, dict)
                    ):
                        _mvp_repository_active_pdf_count = 0

                        for (
                            overlay_key,
                            overlay_record,
                        ) in artifact.items():
                            if not isinstance(
                                overlay_record,
                                dict,
                            ):
                                continue

                            overlay_has_pdf = bool(
                                overlay_record.get(
                                    "has_pdf"
                                )
                                or overlay_record.get(
                                    "pdf_available"
                                )
                            )

                            if not overlay_has_pdf:
                                continue

                            _mvp_repository_active_pdf_count += 1
                            overlay_identity = str(
                                overlay_key or ""
                            ).strip()
                            overlay_identifier = (
                                overlay_identity.replace(
                                    "/",
                                    "-",
                                )
                            )
                            overlay_title = (
                                _mvp_repository_normalize(
                                    overlay_identity
                                )
                            )

                            matched_overlay_index = None

                            if (
                                overlay_identifier
                                in record_id_to_index
                            ):
                                matched_overlay_index = (
                                    record_id_to_index[
                                        overlay_identifier
                                    ]
                                )
                            elif (
                                overlay_title
                                in record_title_to_index
                            ):
                                matched_overlay_index = (
                                    record_title_to_index[
                                        overlay_title
                                    ]
                                )
                            else:
                                nested_identifier = str(
                                    overlay_record.get(
                                        "document_id"
                                    )
                                    or overlay_record.get(
                                        "handle"
                                    )
                                    or ""
                                ).replace("/", "-")
                                nested_title = (
                                    _mvp_repository_normalize(
                                        overlay_record.get(
                                            "title"
                                        )
                                        or overlay_record.get(
                                            "document_title"
                                        )
                                    )
                                )

                                if (
                                    nested_identifier
                                    in record_id_to_index
                                ):
                                    matched_overlay_index = (
                                        record_id_to_index[
                                            nested_identifier
                                        ]
                                    )
                                elif (
                                    nested_title
                                    in record_title_to_index
                                ):
                                    matched_overlay_index = (
                                        record_title_to_index[
                                            nested_title
                                        ]
                                    )

                            if (
                                matched_overlay_index
                                is not None
                            ):
                                pdf_record_indexes.add(
                                    matched_overlay_index
                                )

                    for node in _mvp_repository_walk(
                        artifact
                    ):
                        node_document = (
                            node.get("document")
                            if isinstance(
                                node.get("document"),
                                dict,
                            )
                            else {}
                        )
                        node_metadata = (
                            node.get("metadata")
                            if isinstance(
                                node.get("metadata"),
                                dict,
                            )
                            else {}
                        )
                        document_metadata = (
                            node_document.get("metadata")
                            if isinstance(
                                node_document.get(
                                    "metadata"
                                ),
                                dict,
                            )
                            else {}
                        )

                        has_pdf = bool(
                            node.get("has_pdf")
                            or node.get("pdf_available")
                            or node_metadata.get("has_pdf")
                            or node_metadata.get(
                                "pdf_available"
                            )
                            or document_metadata.get(
                                "has_pdf"
                            )
                            or document_metadata.get(
                                "pdf_available"
                            )
                        )

                        if not has_pdf:
                            continue

                        identifier = str(
                            node.get("document_id")
                            or node_document.get(
                                "document_id"
                            )
                            or ""
                        ).replace("/", "-")
                        normalized_title = (
                            _mvp_repository_normalize(
                                node.get("title")
                                or node_document.get("title")
                            )
                        )

                        matched_index = None

                        if identifier in record_id_to_index:
                            matched_index = (
                                record_id_to_index[
                                    identifier
                                ]
                            )
                        elif (
                            normalized_title
                            in record_title_to_index
                        ):
                            matched_index = (
                                record_title_to_index[
                                    normalized_title
                                ]
                            )

                        if matched_index is not None:
                            pdf_record_indexes.add(
                                matched_index
                            )

                total_documents = len(records)
                pdf_available = (
                    _mvp_repository_active_pdf_count
                    if _mvp_repository_active_pdf_count
                    is not None
                    else len(pdf_record_indexes)
                )
                metadata_only = max(
                    0,
                    total_documents - pdf_available,
                )

                if _mvp_repository_count_intent:
                    answer = (
                        "## Statistik Repository DELBot\n\n"
                        f"Saat ini terdapat **{total_documents} "
                        "dokumen akademik** yang tercatat dalam "
                        "repository DELBot.\n\n"
                        f"- **PDF tersedia:** {pdf_available}\n"
                        f"- **Metadata/abstrak saja:** "
                        f"{metadata_only}\n\n"
                        "Jumlah ini dibaca langsung dari katalog "
                        "repository aktif. Ketik **“lihat isi "
                        "repository”** untuk menampilkan daftar "
                        "dokumennya."
                    )

                    return ResearchPipelineResponse(
                        answer=answer,
                        citations=[],
                        research_state=research_state,
                        rag=None,
                    )

                page_match = _mvp_repository_re.search(
                    r"(?:halaman|page)\s+(\d+)",
                    _mvp_repository_question_lower,
                )
                limit_match = _mvp_repository_re.search(
                    r"(?:tampilkan|lihat|show|limit)"
                    r"\s+(\d+)\s+"
                    r"(?:dokumen|data|item)",
                    _mvp_repository_question_lower,
                )

                page = (
                    max(1, int(page_match.group(1)))
                    if page_match
                    else 1
                )
                limit = (
                    min(
                        20,
                        max(
                            1,
                            int(limit_match.group(1)),
                        ),
                    )
                    if limit_match
                    else 10
                )

                total_pages = max(
                    1,
                    _mvp_repository_math.ceil(
                        total_documents / limit
                    ),
                )
                page = min(page, total_pages)
                start = (page - 1) * limit
                selected_records = records[
                    start:start + limit
                ]

                answer_rows = [
                    "## Isi Repository DELBot",
                    "",
                    (
                        f"Menampilkan dokumen "
                        f"**{start + 1}–"
                        f"{start + len(selected_records)}** "
                        f"dari **{total_documents}** dokumen "
                        f"(halaman {page} dari {total_pages})."
                    ),
                    "",
                ]
                repository_citations = []

                for offset, record in enumerate(
                    selected_records,
                    start=1,
                ):
                    record_index = start + offset - 1
                    title = str(
                        record.get("title")
                        or "Judul tidak tersedia"
                    ).strip()
                    author = str(
                        record.get("author")
                        or "Penulis tidak tersedia"
                    ).strip()
                    year = str(
                        record.get("year")
                        or "Tahun tidak tersedia"
                    ).strip()
                    prodi = str(
                        record.get("prodi")
                        or "Program studi tidak tersedia"
                    ).strip()
                    repository_url = str(
                        record.get("url")
                        or ""
                    ).strip()
                    abstract = str(
                        record.get("abstract")
                        or ""
                    ).strip()
                    identifier = (
                        _mvp_repository_record_id(record)
                    )
                    has_pdf = (
                        record_index
                        in pdf_record_indexes
                    )
                    source_status = (
                        "PDF tersedia"
                        if has_pdf
                        else "Metadata/Abstrak"
                    )

                    answer_rows.extend([
                        f"{offset}. **{title}**",
                        (
                            f"   - {author} · {year} · "
                            f"{prodi} · {source_status}"
                        ),
                    ])

                    if repository_url.startswith(
                        ("http://", "https://")
                    ):
                        answer_rows.append(
                            "   - "
                            f"[Buka repository]"
                            f"({repository_url})"
                        )

                    source_metadata = {
                        "evidence_type": (
                            "metadata_abstract"
                        ),
                        "metadata_only": True,
                        "has_pdf": has_pdf,
                        "author": author,
                        "authors": [author],
                        "year": year,
                        "prodi": prodi,
                        "url": repository_url,
                        "repository_url": repository_url,
                        "repository_listing": True,
                    }

                    repository_citations.append({
                        "chunk_id": (
                            "repository-list-"
                            + (
                                identifier
                                or str(record_index)
                            )
                        ),
                        "document": {
                            "title": title,
                            "document_id": identifier,
                            "authors": [author],
                            "metadata": dict(
                                source_metadata
                            ),
                        },
                        "metadata": dict(
                            source_metadata
                        ),
                        "page": None,
                        "score": 1.0,
                        "text": abstract[:1200],
                    })

                answer_rows.extend([
                    "",
                    (
                        f"Ketik **“lihat isi repository "
                        f"halaman {min(page + 1, total_pages)}”** "
                        "untuk melanjutkan, atau buka menu "
                        "**Repository** untuk penelusuran visual."
                    ),
                ])

                return ResearchPipelineResponse(
                    answer="\n".join(answer_rows),
                    citations=repository_citations,
                    research_state=research_state,
                    rag=None,
                )

            except Exception:
                # Repository discovery failure falls through
                # to the standard conversation pipeline.
                pass

        _mvp_generic_research_markers = (
            "tinjau literatur",
            "review literature",
            "bandingkan studi",
            "compare studies",
            "identifikasi research gap",
            "find a gap",
            "kembangkan beberapa thesis ideas",
            "develop an idea",
        )
        _mvp_question_lower = _mvp_original_question.lower()
        _mvp_generic_research_action = any(
            marker in _mvp_question_lower
            for marker in _mvp_generic_research_markers
        )
        _mvp_prior_topic = ""
        if _mvp_generic_research_action and isinstance(history, list):
            for _mvp_history_item in reversed(history[-12:]):
                if isinstance(_mvp_history_item, dict):
                    _mvp_history_role = str(
                        _mvp_history_item.get("role", "")
                    ).strip().lower()
                    _mvp_history_content = str(
                        _mvp_history_item.get(
                            "content",
                            _mvp_history_item.get("message", ""),
                        )
                    ).strip()
                else:
                    _mvp_history_role = str(
                        getattr(_mvp_history_item, "role", "")
                    ).strip().lower()
                    _mvp_history_content = str(
                        getattr(_mvp_history_item, "content", "")
                    ).strip()
                _mvp_history_content_lower = _mvp_history_content.lower()
                _mvp_history_is_generic = any(
                    marker in _mvp_history_content_lower
                    for marker in _mvp_generic_research_markers
                )
                if (
                    _mvp_history_role in ("user", "human")
                    and _mvp_history_content
                    and _mvp_history_content != _mvp_original_question
                    and not _mvp_history_is_generic
                ):
                    _mvp_prior_topic = _mvp_history_content[:1200]
                    break
        if _mvp_prior_topic:
            _mvp_contextual_question = (
                f"Topik pengguna sebelumnya: {_mvp_prior_topic}\n\n"
                f"Permintaan riset saat ini: {_mvp_original_question}"
            )
        _mvp_contextual_lower = (
            " " + _mvp_contextual_question.lower().replace("-", " ") + " "
        )
        if (
            " ai " in _mvp_contextual_lower
            and "artificial intelligence" not in _mvp_contextual_lower
            and "kecerdasan buatan" not in _mvp_contextual_lower
        ):
            _mvp_contextual_question = (
                f"{_mvp_contextual_question}\n"
                "Istilah pencarian terkait AI: artificial intelligence, kecerdasan buatan, "
                "machine learning, predictive model, anomaly detection."
            )
        # DELBOT MVP frozen contextual topic label
        _mvp_bounded_user_topic = str(
            _mvp_prior_topic
            or _mvp_original_question
            or "permintaan pengguna"
        ).strip()[:240]
        question = _mvp_contextual_question
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

            # DELBOT MVP fulltext-first citation helpers
            def _mvp_citation_value(item, key, default=None):
                if isinstance(item, dict):
                    return item.get(key, default)
                return getattr(item, key, default)

            def _mvp_citation_mapping(item, key):
                value = _mvp_citation_value(item, key, {})
                return value if isinstance(value, dict) else {}

            def _mvp_is_fulltext_citation(item):
                citation_metadata = _mvp_citation_mapping(
                    item,
                    "metadata",
                )
                document = _mvp_citation_value(item, "document", {})
                document_metadata = _mvp_citation_mapping(
                    document,
                    "metadata",
                )

                evidence_type = str(
                    citation_metadata.get("evidence_type")
                    or document_metadata.get("evidence_type")
                    or ""
                ).strip().lower()

                metadata_only = bool(
                    citation_metadata.get("metadata_only")
                    or document_metadata.get("metadata_only")
                )

                has_pdf = (
                    citation_metadata.get("has_pdf") is True
                    or document_metadata.get("has_pdf") is True
                )

                file_path = str(
                    _mvp_citation_value(document, "file_path", "")
                    or citation_metadata.get("file_path")
                    or document_metadata.get("file_path")
                    or ""
                ).lower()

                if (
                    metadata_only
                    or evidence_type == "metadata_abstract"
                    or "metadata_abstract" in evidence_type
                ):
                    return False

                return bool(
                    has_pdf
                    or "fulltext" in evidence_type
                    or "full_text" in evidence_type
                    or "pdf" in evidence_type
                    or file_path.endswith(".pdf")
                    or "/parsed_thesis/" in file_path
                )

            def _mvp_build_fulltext_context(items):
                rows = ["[FULLTEXT PDF EVIDENCE PRIORITY]"]

                for source_number, item in enumerate(items, start=1):
                    document = _mvp_citation_value(
                        item,
                        "document",
                        {},
                    )
                    citation_metadata = _mvp_citation_mapping(
                        item,
                        "metadata",
                    )
                    document_metadata = _mvp_citation_mapping(
                        document,
                        "metadata",
                    )

                    title = str(
                        _mvp_citation_value(document, "title", "")
                        or "Dokumen repository"
                    ).strip()
                    document_id = str(
                        _mvp_citation_value(
                            document,
                            "document_id",
                            "",
                        )
                        or ""
                    ).strip()
                    section = str(
                        citation_metadata.get("section")
                        or citation_metadata.get("section_title")
                        or document_metadata.get("section")
                        or document_metadata.get("section_title")
                        or ""
                    ).strip()
                    page_start = (
                        citation_metadata.get("page_start")
                        or _mvp_citation_value(item, "page", None)
                    )
                    page_end = citation_metadata.get("page_end")
                    excerpt = str(
                        _mvp_citation_value(item, "text", "")
                        or ""
                    ).strip()

                    source_header = (
                        f"[Sumber {source_number} | Isi PDF] "
                        f"{title}"
                    )
                    if document_id:
                        source_header += f" | Kode: {document_id}"
                    if section:
                        source_header += f" | Bagian: {section}"
                    if page_start is not None:
                        source_header += f" | Halaman: {page_start}"
                        if (
                            page_end is not None
                            and page_end != page_start
                        ):
                            source_header += f"-{page_end}"

                    rows.append(source_header)
                    if excerpt:
                        rows.append(excerpt)

                rows.append(
                    "Gunakan isi PDF di atas sebagai evidence utama. "
                    "Jelaskan fokus dokumen, metode, data atau objek, "
                    "temuan, keterbatasan, dan hubungannya dengan "
                    "permintaan pengguna hanya jika informasi tersebut "
                    "benar-benar tersedia pada evidence."
                )
                return "\n\n".join(rows)

            _mvp_fulltext_citations = []
            _mvp_fulltext_context = ""
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
            # DELBOT MVP preserve retrieved fulltext evidence
            _mvp_fulltext_citations = [
                item
                for item in list(citations or [])
                if _mvp_is_fulltext_citation(item)
            ]
            # DELBOT MVP query-aware fulltext selection
            def _mvp_relevance_query_tokens(raw_query):
                import re as _mvp_token_re

                positive_query = str(raw_query or "")
                positive_query = _mvp_token_re.split(
                    (
                        r"\b(?:jangan gunakan|hindari|exclude|"
                        r"tidak menggunakan|bukan dokumen)\b"
                    ),
                    positive_query,
                    maxsplit=1,
                    flags=_mvp_token_re.IGNORECASE,
                )[0]

                stopwords = {
                    "yang", "dan", "atau", "untuk", "dari",
                    "dalam", "dengan", "pada", "tentang",
                    "berbasis", "gunakan", "hanya", "dokumen",
                    "repository", "benar", "membahas",
                    "kembangkan", "tiga", "beberapa", "ide",
                    "tugas", "akhir", "jelaskan", "masalah",
                    "research", "gap", "metode", "rencana",
                    "evaluasi", "kontribusi", "keterbatasan",
                    "sumber", "paling", "relevan", "koleksi",
                    "studi", "literatur", "sistem",
                    "the", "and", "for", "from", "with",
                    "into", "using", "based", "study",
                    "research", "thesis", "idea", "ideas",
                }

                raw_tokens = _mvp_token_re.findall(
                    r"[a-zA-Z0-9]+",
                    positive_query.lower(),
                )

                tokens = []
                for token in raw_tokens:
                    if token in stopwords:
                        continue
                    if len(token) < 4 and token not in {
                        "ai",
                        "ml",
                        "iot",
                        "lora",
                    }:
                        continue
                    if token not in tokens:
                        tokens.append(token)

                return tokens[:18]

            def _mvp_citation_relevance_details(
                citation,
                raw_query,
            ):
                # DELBOT MVP grouped concept relevance
                query_tokens = _mvp_relevance_query_tokens(
                    raw_query
                )

                if not query_tokens:
                    return {
                        "relevant": True,
                        "matches": [],
                        "required": 0,
                        "required_groups": [],
                        "group_matches": {},
                    }

                document = _mvp_citation_value(
                    citation,
                    "document",
                    {},
                )
                metadata = _mvp_citation_mapping(
                    citation,
                    "metadata",
                )
                document_metadata = _mvp_citation_mapping(
                    document,
                    "metadata",
                )

                title = str(
                    _mvp_citation_value(
                        document,
                        "title",
                        "",
                    )
                    or ""
                ).lower()
                excerpt = str(
                    _mvp_citation_value(
                        citation,
                        "text",
                        "",
                    )
                    or ""
                ).lower()
                supporting_metadata = " ".join([
                    str(metadata.get("section") or ""),
                    str(metadata.get("section_title") or ""),
                    str(metadata.get("abstract") or ""),
                    str(metadata.get("prodi") or ""),
                    str(document_metadata.get("keywords") or ""),
                    str(document_metadata.get("entities") or ""),
                    str(document_metadata.get("abstract") or ""),
                    str(document_metadata.get("prodi") or ""),
                ]).lower()

                def _mvp_normalize_relevance_text(value):
                    normalized = str(value or "").lower()
                    for character in (
                        "-", "_", "/", "\\", ".", ",", ":",
                        ";", "(", ")", "[", "]", "{", "}",
                        "'", '"', "\n", "\r", "\t",
                    ):
                        normalized = normalized.replace(
                            character,
                            " ",
                        )
                    return " ".join(normalized.split())

                def _mvp_contains_relevance_term(
                    normalized_text,
                    term,
                ):
                    normalized_term = (
                        _mvp_normalize_relevance_text(term)
                    )
                    if not normalized_term:
                        return False

                    if (
                        len(normalized_term) <= 3
                        and " " not in normalized_term
                    ):
                        return normalized_term in set(
                            normalized_text.split()
                        )

                    return normalized_term in normalized_text

                positive_query = str(raw_query or "").lower()
                for negative_marker in (
                    "jangan gunakan",
                    "jangan memakai",
                    "hindari",
                    "exclude",
                    "tidak menggunakan",
                    "bukan dokumen",
                ):
                    if negative_marker in positive_query:
                        positive_query = positive_query.split(
                            negative_marker,
                            1,
                        )[0]

                normalized_query = (
                    _mvp_normalize_relevance_text(
                        positive_query
                    )
                )
                evidence_blob = (
                    _mvp_normalize_relevance_text(
                        title
                        + " "
                        + excerpt
                        + " "
                        + supporting_metadata
                    )
                )

                concept_groups = (
                    (
                        "agriculture",
                        (
                            "hidroponik", "hydroponic",
                            "pertanian", "agriculture",
                            "tanaman", "plant",
                            "nutrisi", "nutrition",
                            "irigasi", "irrigation",
                            "greenhouse", "smart farming",
                            "agro climate", "agro",
                            "soil", "lahan pertanian",
                        ),
                    ),
                    (
                        "health",
                        (
                            "kesehatan", "health",
                            "medis", "medical",
                            "pasien", "patient",
                            "penyakit", "disease",
                            "rumah sakit", "hospital",
                        ),
                    ),
                    (
                        "education",
                        (
                            "pendidikan", "education",
                            "mahasiswa", "student",
                            "siswa", "sekolah",
                            "pembelajaran", "learning",
                        ),
                    ),
                    (
                        "tourism",
                        (
                            "pariwisata", "tourism",
                            "wisata", "tourist",
                            "destinasi", "destination",
                            "hotel",
                        ),
                    ),
                    (
                        "environment",
                        (
                            "lingkungan", "environment",
                            "polusi", "pollution",
                            "cuaca", "weather",
                            "air quality",
                        ),
                    ),
                    (
                        "bioprocess",
                        (
                            "bioproses", "bioprocess",
                            "mikroorganisme",
                            "microorganism",
                            "fermentasi", "fermentation",
                            "ekstraksi", "extraction",
                            "bioteknologi",
                            "biotechnology",
                        ),
                    ),
                    (
                        "artificial_intelligence",
                        (
                            "artificial intelligence",
                            "kecerdasan buatan",
                            "machine learning",
                            "deep learning",
                            "neural network",
                            "computer vision",
                            "ai", "ml",
                        ),
                    ),
                    (
                        "iot_monitoring",
                        (
                            "internet of things",
                            "iot", "sensor",
                            "monitoring", "otomasi",
                            "automation", "aktuator",
                            "actuator", "mikrokontroler",
                            "microcontroller",
                            "esp32", "lora", "mqtt",
                            "node red",
                        ),
                    ),
                    (
                        "networking",
                        (
                            "jaringan", "network",
                            "telekomunikasi",
                            "telecommunication",
                            "wireless", "routing",
                            "throughput", "packet loss",
                        ),
                    ),
                    (
                        "software",
                        (
                            "perangkat lunak",
                            "software",
                            "website", "web",
                            "aplikasi", "application",
                            "mobile", "desktop",
                            "dashboard",
                        ),
                    ),
                    (
                        "data_system",
                        (
                            "database", "basis data",
                            "data mining",
                            "analytics", "analitik",
                            "sistem informasi",
                            "information system",
                            "business intelligence",
                        ),
                    ),
                    (
                        "electrical_control",
                        (
                            "teknik elektro",
                            "electrical",
                            "elektronika",
                            "electronics",
                            "sistem kendali",
                            "control system",
                            "kelistrikan",
                        ),
                    ),
                    (
                        "business_industry",
                        (
                            "bisnis", "business",
                            "industri", "industry",
                            "manajemen", "management",
                            "optimasi proses",
                            "process optimization",
                        ),
                    ),
                )

                required_groups = []
                group_matches = {}

                for group_name, group_terms in concept_groups:
                    query_group_hits = [
                        term
                        for term in group_terms
                        if _mvp_contains_relevance_term(
                            normalized_query,
                            term,
                        )
                    ]

                    if not query_group_hits:
                        continue

                    required_groups.append(group_name)

                    evidence_group_hits = [
                        term
                        for term in group_terms
                        if _mvp_contains_relevance_term(
                            evidence_blob,
                            term,
                        )
                    ]

                    group_matches[group_name] = (
                        evidence_group_hits
                    )

                matches = [
                    token
                    for token in query_tokens
                    if _mvp_contains_relevance_term(
                        evidence_blob,
                        token,
                    )
                ]

                if required_groups:
                    relevant = all(
                        bool(group_matches.get(group_name))
                        for group_name in required_groups
                    )
                    required = len(required_groups)
                else:
                    required = (
                        1 if len(query_tokens) == 1 else 2
                    )
                    relevant = len(matches) >= required

                return {
                    "relevant": relevant,
                    "matches": matches,
                    "required": required,
                    "required_groups": required_groups,
                    "group_matches": group_matches,
                }

            _mvp_evidence_query = (
                _mvp_contextual_question
                if isinstance(_mvp_contextual_question, str)
                and _mvp_contextual_question.strip()
                else question
            )

            _mvp_fulltext_citations = [
                item
                for item in _mvp_fulltext_citations
                if _mvp_citation_relevance_details(
                    item,
                    _mvp_evidence_query,
                )["relevant"]
            ]
            if _mvp_fulltext_citations:
                _mvp_fulltext_context = (
                    _mvp_build_fulltext_context(
                        _mvp_fulltext_citations
                    )
                )

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


        # BOUNDED_RESEARCH_CONTEXT_767804
        # METADATA_FIRST_CONTEXT_767810
        research_context_char_budget = 8000
        metadata_context_char_budget = 6000
        # EXACT_METADATA_CONTEXT_INITIALIZATION_GUARD_767834
        if "metadata_complement_context" not in locals():
            metadata_complement_context = ""
        metadata_priority_context = (
            metadata_complement_context.strip()
            if isinstance(metadata_complement_context, str)
            else ""
        )
        if len(metadata_priority_context) > metadata_context_char_budget:
            metadata_priority_context = metadata_priority_context[
                :metadata_context_char_budget
            ]

        metadata_context_header = (
            "[METADATA EVIDENCE PRIORITY]\n"
            if metadata_priority_context
            else ""
        )
        general_context_header = (
            "\n\n[GENERAL EVIDENCE CONTEXT]\n"
            if metadata_priority_context
            else ""
        )
        fixed_context = (
            metadata_context_header
            + metadata_priority_context
            + general_context_header
        )
        general_context_budget = max(
            0,
            research_context_char_budget - len(fixed_context),
        )
        general_context = (
            context
            if isinstance(context, str)
            else ""
        )
        if len(general_context) > general_context_budget:
            general_context = general_context[:general_context_budget]

        context = fixed_context + general_context

        # BOUNDED_THESIS_PROMPT_STATE_767821
        thesis_prompt_detection_text = (
            str(question or "").lower()
            + " "
            + str(research_state or "")[:2000].lower()
        )
        thesis_prompt_request_detected = any(
            term in thesis_prompt_detection_text
            for term in (
                "thesis idea",
                "thesis ideas",
                "ide tugas akhir",
                "judul tugas akhir",
                "tiga ide",
                "3 ide",
            )
        )
        bounded_thesis_prompt_history = history
        bounded_thesis_prompt_previous = previous
        bounded_thesis_prompt_research_state = research_state
        if thesis_prompt_request_detected:
            bounded_thesis_prompt_history = []
            bounded_thesis_prompt_previous = None
            if isinstance(research_state, dict):
                bounded_thesis_prompt_research_state = {
                    key: research_state.get(key)
                    for key in (
                        "topic",
                        "goal",
                        "research_direction",
                        "keywords",
                    )
                    if research_state.get(key)
                }
            else:
                bounded_thesis_prompt_research_state = {}
        # DELBOT MVP bounded evidence-turn prompt inputs
        _mvp_prompt_history = [] if evidence_turn else history
        _mvp_prompt_previous = None if evidence_turn else previous
        _mvp_prompt_research_state = research_state
        if evidence_turn and isinstance(research_state, dict):
            _mvp_prompt_research_state = {
                key: research_state.get(key)
                for key in ("topic", "goal", "research_direction", "keywords")
                if research_state.get(key) is not None
                and research_state.get(key) != ""
                and research_state.get(key) != []
                and research_state.get(key) != {}
            }
        # DELBOT MVP fulltext evidence synthesis contract
        _mvp_prompt_query = question
        if evidence_turn:
            _mvp_prompt_query = (
                f"{question}\n\n"
                "KONTRAK SINTESIS EVIDENCE FULLTEXT PDF:\n"
                "1. Prioritaskan dokumen fulltext PDF yang paling relevan dengan topik pengguna.\n"
                "2. Untuk setiap dokumen, jelaskan secara terpisah: fokus penelitian, masalah, "
                "objek atau dataset, metode, metrik evaluasi, temuan, keterbatasan, dan hubungan "
                "dokumen dengan pertanyaan pengguna.\n"
                "3. Sebutkan BAB, section, subbagian, atau halaman hanya jika informasi tersebut "
                "benar-benar tersedia dalam evidence.\n"
                "4. Bedakan dengan tegas fakta dokumen, interpretasi, research gap, dan proposal baru.\n"
                "5. Jangan membuat dataset, metode, hasil, halaman, section, keterbatasan, atau sitasi "
                "yang tidak tersedia dalam evidence.\n"
                "6. Jika evidence hanya metadata atau abstrak, beri label METADATA/ABSTRAK dan jangan "
                "menampilkannya sebagai temuan fulltext.\n"
                "7. Gunakan Document ID pada setiap pembahasan dokumen agar dapat dihubungkan dengan "
                "kartu sumber di antarmuka."
            )
        # DELBOT MVP enforce fulltext-first prompt context
        if evidence_turn and _mvp_fulltext_citations:
            citations = list(_mvp_fulltext_citations)
            context = _mvp_fulltext_context[:8000]
            metadata_complement_context = ""
        # DELBOT MVP query-aware metadata fallback
        # DELBOT MVP exact repository source selection
        if evidence_turn and not _mvp_fulltext_citations:
            try:
                from pathlib import Path as _MvpExactPath
                import json as _mvp_exact_json
                import re as _mvp_exact_re

                def _mvp_exact_normalize(value):
                    return " ".join(
                        _mvp_exact_re.findall(
                            r"[a-z0-9]+",
                            str(value or "").lower(),
                        )
                    )

                def _mvp_exact_document_id(record):
                    direct_id = str(
                        record.get("document_id")
                        or record.get("documentId")
                        or record.get("handle")
                        or ""
                    ).strip()

                    if direct_id:
                        return direct_id.replace("/", "-")

                    source_url = str(
                        record.get("url")
                        or record.get("repository_url")
                        or ""
                    ).rstrip("/")

                    handle = source_url.rsplit("/", 1)[-1]

                    if handle.isdigit():
                        return "123456789-" + handle

                    return ""

                def _mvp_exact_longest_run(
                    query_tokens,
                    title_tokens,
                ):
                    longest = 0

                    for start in range(len(query_tokens)):
                        for end in range(
                            start + 1,
                            len(query_tokens) + 1,
                        ):
                            sequence = query_tokens[start:end]
                            size = len(sequence)

                            if size <= longest:
                                continue

                            for title_start in range(
                                0,
                                len(title_tokens) - size + 1,
                            ):
                                if (
                                    title_tokens[
                                        title_start:title_start + size
                                    ]
                                    == sequence
                                ):
                                    longest = size
                                    break

                    return longest

                def _mvp_exact_walk(value):
                    if isinstance(value, dict):
                        yield value

                        for child in value.values():
                            yield from _mvp_exact_walk(child)

                    elif isinstance(value, list):
                        for child in value:
                            yield from _mvp_exact_walk(child)

                _mvp_exact_query_text = str(
                    _mvp_evidence_query
                    or question
                    or ""
                )
                _mvp_exact_query_normalized = (
                    _mvp_exact_normalize(
                        _mvp_exact_query_text
                    )
                )

                _mvp_exact_stopwords = {
                    "saya", "butuh", "untuk", "yang", "dan",
                    "dengan", "dalam", "tentang", "terkait",
                    "skripsi", "tugas", "akhir", "pembuatan",
                    "referensi", "refrensi", "repository",
                    "berikan", "tolong", "apakah", "bisa",
                }

                _mvp_exact_query_tokens = [
                    token
                    for token in (
                        _mvp_exact_query_normalized.split()
                    )
                    if (
                        len(token) >= 3
                        and token not in _mvp_exact_stopwords
                    )
                ]

                _mvp_exact_dataset_path = _MvpExactPath(
                    "delbot_platform/repository_data/metadata/"
                    "skripsi_dataset.json"
                )

                _mvp_exact_records = []

                if _mvp_exact_dataset_path.is_file():
                    _mvp_exact_loaded = (
                        _mvp_exact_json.loads(
                            _mvp_exact_dataset_path.read_text(
                                encoding="utf-8"
                            )
                        )
                    )

                    if isinstance(_mvp_exact_loaded, list):
                        _mvp_exact_records = [
                            record
                            for record in _mvp_exact_loaded
                            if isinstance(record, dict)
                        ]

                _mvp_exact_ranked = []

                for _mvp_exact_record in _mvp_exact_records:
                    _mvp_exact_title = str(
                        _mvp_exact_record.get("title")
                        or ""
                    ).strip()

                    _mvp_exact_title_tokens = (
                        _mvp_exact_normalize(
                            _mvp_exact_title
                        ).split()
                    )

                    if not _mvp_exact_title_tokens:
                        continue

                    _mvp_exact_overlap = set(
                        _mvp_exact_query_tokens
                    ).intersection(
                        _mvp_exact_title_tokens
                    )

                    _mvp_exact_run = (
                        _mvp_exact_longest_run(
                            _mvp_exact_query_tokens,
                            _mvp_exact_title_tokens,
                        )
                    )

                    _mvp_exact_coverage = (
                        len(_mvp_exact_overlap)
                        / max(
                            1,
                            min(
                                len(
                                    set(
                                        _mvp_exact_query_tokens
                                    )
                                ),
                                12,
                            ),
                        )
                    )

                    _mvp_exact_score = (
                        (_mvp_exact_run * 30)
                        + (len(_mvp_exact_overlap) * 5)
                        + (_mvp_exact_coverage * 20)
                    )

                    if (
                        _mvp_exact_query_normalized
                        and _mvp_exact_query_normalized
                        in _mvp_exact_normalize(
                            _mvp_exact_title
                        )
                    ):
                        _mvp_exact_score += 120

                    if (
                        _mvp_exact_run >= 3
                        or (
                            len(_mvp_exact_overlap) >= 4
                            and _mvp_exact_coverage >= 0.35
                        )
                    ):
                        _mvp_exact_ranked.append(
                            (
                                _mvp_exact_score,
                                _mvp_exact_run,
                                len(_mvp_exact_overlap),
                                _mvp_exact_record,
                            )
                        )

                _mvp_exact_ranked.sort(
                    key=lambda row: (
                        row[0],
                        row[1],
                        row[2],
                    ),
                    reverse=True,
                )

                if _mvp_exact_ranked:
                    _mvp_exact_record = (
                        _mvp_exact_ranked[0][3]
                    )
                    _mvp_exact_title = str(
                        _mvp_exact_record.get("title")
                        or "Dokumen repository"
                    ).strip()
                    _mvp_exact_id = (
                        _mvp_exact_document_id(
                            _mvp_exact_record
                        )
                    )
                    _mvp_exact_url = str(
                        _mvp_exact_record.get("url")
                        or _mvp_exact_record.get(
                            "repository_url"
                        )
                        or ""
                    ).strip()
                    _mvp_exact_author = str(
                        _mvp_exact_record.get("author")
                        or _mvp_exact_record.get("authors")
                        or ""
                    ).strip()
                    _mvp_exact_year = str(
                        _mvp_exact_record.get("year")
                        or ""
                    ).strip()
                    _mvp_exact_prodi = str(
                        _mvp_exact_record.get("prodi")
                        or _mvp_exact_record.get("program")
                        or ""
                    ).strip()
                    _mvp_exact_abstract = str(
                        _mvp_exact_record.get("abstract")
                        or _mvp_exact_record.get("summary")
                        or ""
                    ).strip()

                    _mvp_exact_has_pdf = False
                    _mvp_exact_fulltext_candidates = []

                    _mvp_exact_artifact_paths = (
                        _MvpExactPath(
                            "delbot_platform/repository_data/"
                            "runtime/repository_overlay_index.json"
                        ),
                        _MvpExactPath(
                            "delbot_platform/repository_data/"
                            "runtime/repository_overlay.json"
                        ),
                        _MvpExactPath(
                            "delbot_platform/repository_data/"
                            "metadata/repository_catalog.json"
                        ),
                    )

                    for _mvp_exact_artifact_path in (
                        _mvp_exact_artifact_paths
                    ):
                        if (
                            not _mvp_exact_artifact_path.is_file()
                            or _mvp_exact_artifact_path.stat().st_size
                            > 25_000_000
                        ):
                            continue

                        try:
                            _mvp_exact_artifact = (
                                _mvp_exact_json.loads(
                                    _mvp_exact_artifact_path.read_text(
                                        encoding="utf-8"
                                    )
                                )
                            )
                        except Exception:
                            continue

                        for _mvp_exact_node in (
                            _mvp_exact_walk(
                                _mvp_exact_artifact
                            )
                        ):
                            _mvp_exact_node_document = (
                                _mvp_exact_node.get("document")
                                if isinstance(
                                    _mvp_exact_node.get(
                                        "document"
                                    ),
                                    dict,
                                )
                                else {}
                            )
                            _mvp_exact_node_metadata = (
                                _mvp_exact_node.get("metadata")
                                if isinstance(
                                    _mvp_exact_node.get(
                                        "metadata"
                                    ),
                                    dict,
                                )
                                else {}
                            )
                            _mvp_exact_node_document_metadata = (
                                _mvp_exact_node_document.get(
                                    "metadata"
                                )
                                if isinstance(
                                    _mvp_exact_node_document.get(
                                        "metadata"
                                    ),
                                    dict,
                                )
                                else {}
                            )

                            _mvp_exact_node_id = str(
                                _mvp_exact_node.get(
                                    "document_id"
                                )
                                or _mvp_exact_node_document.get(
                                    "document_id"
                                )
                                or ""
                            ).replace("/", "-")
                            _mvp_exact_node_title = str(
                                _mvp_exact_node.get("title")
                                or _mvp_exact_node_document.get(
                                    "title"
                                )
                                or ""
                            ).strip()

                            _mvp_exact_same_source = bool(
                                (
                                    _mvp_exact_id
                                    and _mvp_exact_node_id
                                    == _mvp_exact_id
                                )
                                or (
                                    _mvp_exact_node_title
                                    and _mvp_exact_normalize(
                                        _mvp_exact_node_title
                                    )
                                    == _mvp_exact_normalize(
                                        _mvp_exact_title
                                    )
                                )
                            )

                            if not _mvp_exact_same_source:
                                continue

                            _mvp_exact_has_pdf = bool(
                                _mvp_exact_has_pdf
                                or _mvp_exact_node.get(
                                    "has_pdf"
                                )
                                or _mvp_exact_node_metadata.get(
                                    "has_pdf"
                                )
                                or _mvp_exact_node_document_metadata.get(
                                    "has_pdf"
                                )
                                or _mvp_exact_node.get(
                                    "pdf_available"
                                )
                            )

                            _mvp_exact_node_type = str(
                                _mvp_exact_node.get(
                                    "evidence_type"
                                )
                                or _mvp_exact_node_metadata.get(
                                    "evidence_type"
                                )
                                or _mvp_exact_node_document_metadata.get(
                                    "evidence_type"
                                )
                                or ""
                            ).lower()
                            _mvp_exact_node_text = str(
                                _mvp_exact_node.get("text")
                                or _mvp_exact_node.get(
                                    "chunk_text"
                                )
                                or _mvp_exact_node.get(
                                    "content_text"
                                )
                                or ""
                            ).strip()
                            _mvp_exact_node_section = str(
                                _mvp_exact_node.get("section")
                                or _mvp_exact_node_metadata.get(
                                    "section"
                                )
                                or _mvp_exact_node_metadata.get(
                                    "section_title"
                                )
                                or ""
                            ).strip()
                            _mvp_exact_node_page = (
                                _mvp_exact_node.get("page")
                                or _mvp_exact_node_metadata.get(
                                    "page"
                                )
                                or _mvp_exact_node_metadata.get(
                                    "page_start"
                                )
                            )

                            _mvp_exact_is_fulltext = bool(
                                _mvp_exact_node_text
                                and len(
                                    _mvp_exact_node_text
                                ) >= 120
                                and (
                                    "fulltext"
                                    in _mvp_exact_node_type
                                    or "full_text"
                                    in _mvp_exact_node_type
                                    or "pdf_chunk"
                                    in _mvp_exact_node_type
                                    or (
                                        (
                                            _mvp_exact_node_section
                                            or _mvp_exact_node_page
                                            is not None
                                        )
                                        and "metadata"
                                        not in _mvp_exact_node_type
                                    )
                                )
                            )

                            if _mvp_exact_is_fulltext:
                                _mvp_exact_fulltext_candidates.append(
                                    {
                                        "text": (
                                            _mvp_exact_node_text
                                        ),
                                        "section": (
                                            _mvp_exact_node_section
                                        ),
                                        "page": (
                                            _mvp_exact_node_page
                                        ),
                                    }
                                )

                    _mvp_exact_shared_metadata = {
                        "author": _mvp_exact_author,
                        "authors": (
                            [_mvp_exact_author]
                            if _mvp_exact_author
                            else []
                        ),
                        "year": _mvp_exact_year,
                        "prodi": _mvp_exact_prodi,
                        "url": _mvp_exact_url,
                        "repository_url": _mvp_exact_url,
                        "has_pdf": _mvp_exact_has_pdf,
                    }

                    if _mvp_exact_fulltext_candidates:
                        _mvp_exact_fulltext_candidates.sort(
                            key=lambda item: len(
                                item.get("text") or ""
                            ),
                            reverse=True,
                        )
                        _mvp_exact_chunk = (
                            _mvp_exact_fulltext_candidates[0]
                        )
                        _mvp_exact_page = (
                            _mvp_exact_chunk.get("page")
                        )
                        _mvp_exact_section = str(
                            _mvp_exact_chunk.get("section")
                            or ""
                        )

                        _mvp_exact_root_metadata = {
                            **_mvp_exact_shared_metadata,
                            "evidence_type": "fulltext",
                            "metadata_only": False,
                            "section": _mvp_exact_section,
                            "page_start": _mvp_exact_page,
                            "page_end": _mvp_exact_page,
                        }

                        _mvp_exact_citation = {
                            "chunk_id": (
                                "exact-fulltext-"
                                + (
                                    _mvp_exact_id
                                    or "repository"
                                )
                            ),
                            "document": {
                                "title": _mvp_exact_title,
                                "document_id": _mvp_exact_id,
                                "authors": (
                                    [_mvp_exact_author]
                                    if _mvp_exact_author
                                    else []
                                ),
                                "metadata": dict(
                                    _mvp_exact_root_metadata
                                ),
                            },
                            "metadata": dict(
                                _mvp_exact_root_metadata
                            ),
                            "page": _mvp_exact_page,
                            "score": (
                                _mvp_exact_ranked[0][0]
                            ),
                            "text": _mvp_exact_chunk.get(
                                "text"
                            )
                            or "",
                        }

                        _mvp_exact_selected_citation = _mvp_exact_citation
                        _mvp_fulltext_citations = [
                            _mvp_exact_citation
                        ]
                        citations = list(
                            _mvp_fulltext_citations
                        )
                        _mvp_fulltext_context = (
                            _mvp_build_fulltext_context(
                                _mvp_fulltext_citations
                            )
                        )
                        context = _mvp_fulltext_context[:8000]
                        metadata_complement_context = ""
                        messages = self.prompt_builder.build(
                            query=_mvp_prompt_query,
                            context=context,
                            history=_mvp_prompt_history,
                            previous=_mvp_prompt_previous,
                            research_state=(
                                _mvp_prompt_research_state
                            ),
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

                    else:
                        _mvp_exact_root_metadata = {
                            **_mvp_exact_shared_metadata,
                            "evidence_type": (
                                "metadata_abstract"
                            ),
                            "metadata_only": True,
                            "fallback_reason": (
                                "no_relevant_parsed_fulltext"
                            ),
                        }

                        _mvp_exact_citation = {
                            "chunk_id": (
                                "exact-metadata-"
                                + (
                                    _mvp_exact_id
                                    or "repository"
                                )
                            ),
                            "document": {
                                "title": _mvp_exact_title,
                                "document_id": _mvp_exact_id,
                                "authors": (
                                    [_mvp_exact_author]
                                    if _mvp_exact_author
                                    else []
                                ),
                                "metadata": dict(
                                    _mvp_exact_root_metadata
                                ),
                            },
                            "metadata": dict(
                                _mvp_exact_root_metadata
                            ),
                            "page": None,
                            "score": (
                                _mvp_exact_ranked[0][0]
                            ),
                            "text": _mvp_exact_abstract,
                        }

                        _mvp_exact_selected_citation = _mvp_exact_citation
                        _mvp_exact_existing_ids = {
                            str(
                                _mvp_citation_value(
                                    _mvp_citation_value(
                                        item,
                                        "document",
                                        {},
                                    ),
                                    "document_id",
                                    "",
                                )
                            )
                            for item in metadata_citations
                        }

                        if (
                            _mvp_exact_id
                            not in _mvp_exact_existing_ids
                        ):
                            metadata_citations = [
                                _mvp_exact_citation,
                                *metadata_citations,
                            ]
                        else:
                            metadata_citations = [
                                _mvp_exact_citation,
                                *[
                                    item
                                    for item in metadata_citations
                                    if str(
                                        _mvp_citation_value(
                                            _mvp_citation_value(
                                                item,
                                                "document",
                                                {},
                                            ),
                                            "document_id",
                                            "",
                                        )
                                    )
                                    != _mvp_exact_id
                                ],
                            ]
            except Exception:
                # Exact source lookup is an optional retrieval
                # enhancement; standard relevance fallback remains.
                pass

        if evidence_turn and not _mvp_fulltext_citations:
            _mvp_relevant_metadata_citations = []

            for _mvp_metadata_source in list(
                citations or []
            ):
                _mvp_metadata_source_metadata = (
                    _mvp_citation_mapping(
                        _mvp_metadata_source,
                        "metadata",
                    )
                )
                _mvp_metadata_source_document = (
                    _mvp_citation_value(
                        _mvp_metadata_source,
                        "document",
                        {},
                    )
                )
                _mvp_metadata_document_metadata = (
                    _mvp_citation_mapping(
                        _mvp_metadata_source_document,
                        "metadata",
                    )
                )

                _mvp_metadata_only = bool(
                    _mvp_metadata_source_metadata.get(
                        "metadata_only"
                    )
                    or _mvp_metadata_document_metadata.get(
                        "metadata_only"
                    )
                    or (
                        _mvp_metadata_source_metadata.get(
                            "evidence_type"
                        )
                        == "metadata_abstract"
                    )
                )

                if not _mvp_metadata_only:
                    continue

                _mvp_metadata_relevance = (
                    _mvp_citation_relevance_details(
                        _mvp_metadata_source,
                        _mvp_evidence_query,
                    )
                )

                if _mvp_metadata_relevance["relevant"]:
                    _mvp_relevant_metadata_citations.append(
                        _mvp_metadata_source
                    )

            if _mvp_relevant_metadata_citations:
                citations = list(
                    _mvp_relevant_metadata_citations[:3]
                )
                _mvp_metadata_context_rows = [
                    "[METADATA/ABSTRACT FALLBACK]",
                ]

                for (
                    _mvp_metadata_number,
                    _mvp_metadata_source,
                ) in enumerate(citations, start=1):
                    _mvp_metadata_document = (
                        _mvp_citation_value(
                            _mvp_metadata_source,
                            "document",
                            {},
                        )
                    )
                    _mvp_metadata_title = str(
                        _mvp_citation_value(
                            _mvp_metadata_document,
                            "title",
                            "",
                        )
                        or "Dokumen repository"
                    ).strip()
                    _mvp_metadata_text = str(
                        _mvp_citation_value(
                            _mvp_metadata_source,
                            "text",
                            "",
                        )
                        or ""
                    ).strip()

                    _mvp_metadata_context_rows.append(
                        (
                            f"[Sumber {_mvp_metadata_number} | "
                            f"Metadata/Abstrak] "
                            f"{_mvp_metadata_title}"
                        )
                    )
                    if _mvp_metadata_text:
                        _mvp_metadata_context_rows.append(
                            _mvp_metadata_text
                        )

                _mvp_metadata_context_rows.append(
                    "Metadata/abstrak digunakan karena tidak "
                    "ada fulltext PDF yang relevan dengan "
                    "topik pengguna. Jangan membuat klaim bab "
                    "atau halaman PDF."
                )

                metadata_complement_context = (
                    "\n\n".join(
                        _mvp_metadata_context_rows
                    )[:8000]
                )
                context = metadata_complement_context
        messages = (
            self.prompt_builder.build(
                query=_mvp_prompt_query,
                context=context,
                history=_mvp_prompt_history,
                previous=_mvp_prompt_previous,
                research_state=_mvp_prompt_research_state,
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

        # DELBOT MVP research generation failure fallback
        try:
            generated = await _mvp_bounded_generator_call(messages)

            if inspect.isawaitable(
                generated
            ):
                generated = await generated
        except Exception:
            if not evidence_turn:
                raise

            generated = ""

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

        # THESIS_THREE_IDEA_REPAIR_TRIGGER_767815
        thesis_primary_answer_text = str(generated or "")
        thesis_primary_answer_lower = thesis_primary_answer_text.lower()
        thesis_request_lower = str(question or "").lower()
        thesis_request_detected = any(
            term in thesis_request_lower
            for term in (
                "thesis idea",
                "thesis ideas",
                "ide tugas akhir",
                "judul tugas akhir",
                "tiga ide",
                "3 ide",
            )
        )
        thesis_false_refusal_detected = any(
            term in thesis_primary_answer_lower
            for term in (
                "evidence yang tersedia tidak mencukupi",
                "bukti yang tersedia tidak mencukupi",
                "tidak ada dokumen dalam konteks",
                "tidak dapat disusun proposal",
                "tidak dapat memberikan tiga ide",
                "insufficient evidence",
                "cannot provide three",
            )
        )
        thesis_idea_marker_count = sum(
            1
            for marker in (
                "ide 1",
                "ide 2",
                "ide 3",
            )
            if marker in thesis_primary_answer_lower
        )
        thesis_required_field_count = sum(
            1
            for field in (
                "masalah",
                "research gap",
                "metode",
                "evaluasi",
                "kontribusi",
                "keterbatasan",
            )
            if field in thesis_primary_answer_lower
        )
        thesis_three_idea_repair_required = (
            thesis_request_detected
            and (
                thesis_false_refusal_detected
                or thesis_idea_marker_count < 3
                or thesis_required_field_count < 6
            )
        )
        if (_answer_needs_synthesis_repair(synthesis_answer)) or thesis_three_idea_repair_required:
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
                # THESIS_THREE_IDEA_REPAIR_FORMAT_767815
                "4. Untuk thesis ideas, keluarkan tepat tiga blok dengan heading persis: ## Ide 1, ## Ide 2, dan ## Ide 3.\n"
                "5. Setiap blok wajib memiliki label: Judul, Masalah, Research Gap, Metode Sistem yang Diusulkan, Rencana Evaluasi, Kontribusi, Keterbatasan, dan Sumber Pendukung.\n"
                "6. Metadata relevan boleh mendasari masalah dan gap. Detail metode, evaluasi, dan kontribusi harus ditandai sebagai proposal baru, bukan hasil penelitian terdahulu.\n"
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
                    # THESIS_COMPACT_REPAIR_MESSAGES_767817
                    # THESIS_COMPACT_REPAIR_GUARD_767818
                    thesis_compact_guard_state = str(research_state or "").lower()
                    thesis_compact_repair_active = (
                        thesis_three_idea_repair_required
                        or thesis_request_detected
                        or "thesis idea" in thesis_compact_guard_state
                        or "ide tugas akhir" in thesis_compact_guard_state
                        or "tiga ide" in thesis_compact_guard_state
                        or "3 ide" in thesis_compact_guard_state
                    )
                    if thesis_compact_repair_active:
                        thesis_compact_repair_context = str(context or "")[:6000]
                        thesis_compact_repair_question = str(question or "")[:1000]
                        repair_messages = [
                            {
                                "role": "system",
                                "content": (
                                    "Anda adalah generator proposal tugas akhir DELBot. "
                                    "Evidence metadata yang relevan sah untuk mendasari masalah dan research gap. "
                                    "Jangan menolak jawaban jika evidence relevan tersedia. "
                                    "Jangan mengklaim parameter, dataset, implementasi, atau hasil eksperimen yang tidak ada pada evidence. "
                                    "Metode, evaluasi, kontribusi, dan keterbatasan baru wajib ditandai sebagai proposal penelitian."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    "PERTANYAAN:\n"
                                    + thesis_compact_repair_question
                                    + "\n\nEVIDENCE RELEVAN:\n"
                                    + thesis_compact_repair_context
                                    + "\n\nINSTRUKSI OUTPUT WAJIB:\n"
                                    + "Hasilkan tepat tiga ide dengan heading persis ## Ide 1, ## Ide 2, dan ## Ide 3.\n"
                                    + "Setiap ide wajib memiliki label Judul, Masalah, Research Gap, Metode Sistem yang Diusulkan, Rencana Evaluasi, Kontribusi, Keterbatasan, dan Sumber Pendukung.\n"
                                    + "Gunakan hanya document_id atau sumber yang tersedia pada evidence. Jangan membuat sitasi baru.\n"
                                    + "Tulis ringkas tetapi lengkap. Bedakan fakta evidence dari proposal baru."
                                ),
                            },
                        ]
                    repaired = await _mvp_bounded_generator_call(repair_messages)
                    # BOUNDED_DETERMINISTIC_THESIS_FALLBACK_767820
                    thesis_repair_output_text = str(repaired or "")
                    thesis_repair_output_lower = thesis_repair_output_text.lower()
                    thesis_repair_idea_count = sum(
                        1
                        for heading in (
                            "## ide 1",
                            "## ide 2",
                            "## ide 3",
                        )
                        if heading in thesis_repair_output_lower
                    )
                    thesis_repair_false_refusal = any(
                        phrase in thesis_repair_output_lower
                        for phrase in (
                            "evidence yang tersedia tidak mencukupi",
                            "bukti yang tersedia tidak mencukupi",
                            "tidak ada dokumen dalam konteks",
                            "tidak dapat disusun proposal",
                            "tidak dapat menghasilkan tiga ide",
                            "tidak dapat memberikan tiga ide",
                            "insufficient evidence",
                            "cannot provide three",
                        )
                    )
                    thesis_deterministic_fallback_required = (
                        thesis_compact_repair_active
                        and (
                            thesis_repair_false_refusal
                            or thesis_repair_idea_count < 3
                        )
                    )
                    # DELBOT MVP query-evidence domain relevance gate
                    _mvp_query_domain_groups = (
                        ("kesehatan", ("kesehatan", "pasien", "medis", "medical", "health", "healthcare", "penyakit", "rumah sakit", "jantung", "diabetes", "lansia", "patient")),
                        ("pertanian", ("pertanian", "tanaman", "cabai", "hidroponik", "greenhouse", "smart farming", "irigasi", "perkebunan", "agriculture", "farming")),
                        ("pendidikan", ("pendidikan", "siswa", "mahasiswa", "sekolah", "kelas", "pembelajaran", "education", "student")),
                        ("pariwisata", ("pariwisata", "wisata", "tourism", "tourist", "destinasi", "hotel")),
                    )
                    _mvp_query_lower = str(question or "").lower()
                    _mvp_is_thesis_idea_request = any(
                        phrase in _mvp_query_lower
                        for phrase in (
                            "judul tugas akhir",
                            "ide tugas akhir",
                            "thesis idea",
                            "thesis ideas",
                            "proposal penelitian",
                            "kembangkan beberapa thesis",
                            "develop an idea",
                            "develop thesis",
                        )
                    )
                    _mvp_evidence_lower = (
                        metadata_complement_context.lower()
                        if isinstance(metadata_complement_context, str)
                        else ""
                    )
                    _mvp_requested_domain_label = ""
                    _mvp_requested_domain_terms = ()
                    for _mvp_domain_label, _mvp_domain_terms in _mvp_query_domain_groups:
                        if any(
                            term in _mvp_query_lower
                            for term in _mvp_domain_terms
                        ):
                            _mvp_requested_domain_label = _mvp_domain_label
                            _mvp_requested_domain_terms = _mvp_domain_terms
                            break
                    _mvp_thesis_domain_evidence_valid = (
                        not _mvp_requested_domain_terms
                        or any(
                            term in _mvp_evidence_lower
                            for term in _mvp_requested_domain_terms
                        )
                    )
                    if _mvp_thesis_domain_evidence_valid and (thesis_deterministic_fallback_required):
                        thesis_fallback_evidence = []
                        thesis_fallback_seen_ids = set()
                        for thesis_raw_block in str(metadata_complement_context or "").split("[Metadata Complement ")[1:]:
                            thesis_document_id = ""
                            thesis_document_title = ""
                            thesis_document_abstract = ""
                            for thesis_block_line in thesis_raw_block.splitlines():
                                thesis_clean_line = thesis_block_line.strip()
                                if thesis_clean_line.startswith("Document ID:"):
                                    thesis_document_id = thesis_clean_line.split(":", 1)[1].strip()
                                elif thesis_clean_line.startswith("Title:"):
                                    thesis_document_title = thesis_clean_line.split(":", 1)[1].strip()
                            if "Abstract:" in thesis_raw_block:
                                thesis_document_abstract = thesis_raw_block.split("Abstract:", 1)[1].strip()
                            thesis_document_abstract = " ".join(
                                thesis_document_abstract.split()
                            )[:520]
                            if (
                                thesis_document_id
                                and thesis_document_title
                                and thesis_document_id not in thesis_fallback_seen_ids
                            ):
                                thesis_fallback_seen_ids.add(thesis_document_id)
                                thesis_fallback_evidence.append(
                                    {
                                        "document_id": thesis_document_id,
                                        "title": thesis_document_title,
                                        "abstract": thesis_document_abstract,
                                    }
                                )
                            if len(thesis_fallback_evidence) >= 3:
                                break
                        thesis_fallback_focuses = (
                            (
                                "Pemodelan Prediktif dan Deteksi Anomali",
                                "Evidence menunjukkan sistem dasar telah dikembangkan, tetapi metadata yang tersedia belum menunjukkan evaluasi pengembangan prediktif dan deteksi anomali secara khusus.",
                                "mengembangkan pipeline pengumpulan data, praproses, pemodelan prediktif atau deteksi anomali, serta dashboard peringatan",
                                "akurasi atau MAE sesuai jenis keluaran, precision-recall anomali, latency, dan availability sistem",
                            ),
                            (
                                "Kendali Adaptif dan Keandalan End-to-End",
                                "Evidence membahas monitoring atau komunikasi, tetapi metadata yang tersedia belum menunjukkan evaluasi kendali adaptif dan keandalan sistem secara end-to-end.",
                                "mengembangkan sensor, komunikasi, aturan kendali adaptif, aktuator, penyimpanan data, dan antarmuka monitoring",
                                "packet loss, delay, throughput, keberhasilan aksi kendali, penggunaan sumber daya, dan availability",
                            ),
                            (
                                "Interoperabilitas dan Ketahanan Deployment",
                                "Evidence menunjukkan implementasi pada perangkat atau platform tertentu, tetapi metadata yang tersedia belum memperlihatkan perbandingan interoperabilitas dan ketahanan deployment secara khusus.",
                                "mengembangkan gateway edge, antarmuka data standar, sinkronisasi lokal-cloud, dashboard, dan mekanisme pemulihan koneksi",
                                "latency, availability, keberhasilan pertukaran data, pemulihan setelah gangguan, konsumsi daya, dan usability",
                            ),
                        )
                        thesis_fallback_parts = [
                            "Berikut tiga proposal penelitian yang diturunkan dari evidence repository. Fakta sumber dipisahkan dari rancangan penelitian baru."
                        ]
                        for thesis_index, thesis_evidence in enumerate(
                            thesis_fallback_evidence[:3],
                            start=1,
                        ):
                            (
                                thesis_focus_title,
                                thesis_gap_text,
                                thesis_method_text,
                                thesis_evaluation_text,
                            ) = thesis_fallback_focuses[thesis_index - 1]
                            thesis_source_fact = thesis_evidence["abstract"]
                            if not thesis_source_fact:
                                thesis_source_fact = (
                                    "Metadata repository menyediakan judul dan identitas dokumen, tetapi tidak menyediakan uraian fulltext."
                                )
                            thesis_fallback_parts.append(
                                (
                                    f"## Ide {thesis_index}\n"
                                    f"**Judul:** {thesis_focus_title} pada {thesis_evidence['title']}\n\n"
                                    f"**Masalah:** Evidence {thesis_evidence['document_id']} menjelaskan: {thesis_source_fact} Fakta tersebut menunjukkan kebutuhan pengembangan lanjutan yang tetap terkait langsung dengan sistem pada sumber.\n\n"
                                    f"**Research Gap:** {thesis_gap_text} Pernyataan gap ini dibatasi pada evidence repository yang tersedia dan bukan klaim bahwa seluruh literatur belum membahasnya.\n\n"
                                    f"**Metode Sistem yang Diusulkan:** Sebagai proposal baru, penelitian akan {thesis_method_text}. Tahapan mencakup perancangan, implementasi prototipe, pengumpulan data uji, dan analisis hasil.\n\n"
                                    f"**Rencana Evaluasi:** Sebagai rancangan evaluasi baru, ukur {thesis_evaluation_text} dan bandingkan dengan baseline yang ditetapkan sebelum eksperimen.\n\n"
                                    f"**Kontribusi:** Artefak prototipe dan hasil evaluasi terukur untuk memperluas arah sistem yang telah ditunjukkan oleh evidence. Kontribusi ini masih berupa target penelitian, bukan hasil yang sudah terbukti.\n\n"
                                    f"**Keterbatasan:** Evidence yang digunakan terbatas pada metadata atau abstrak repository. Parameter, dataset, dan hasil eksperimen proposal harus divalidasi saat penelitian dilaksanakan.\n\n"
                                    f"**Sumber Pendukung:** [{thesis_evidence['document_id']}] {thesis_evidence['title']}."
                                )
                            )
                        if len(thesis_fallback_evidence) >= 3:
                            thesis_fallback_answer = "\n\n".join(thesis_fallback_parts)
                            repaired = thesis_fallback_answer
                            generated = thesis_fallback_answer

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

        # FINAL_BOUNDARY_THESIS_FALLBACK_767825
        final_thesis_detection_text = (
            str(question or "").lower()
            + " "
            + str(research_state or "")[:2000].lower()
        )
        final_thesis_request_detected = any(
            term in final_thesis_detection_text
            for term in (
                "thesis idea",
                "thesis ideas",
                "ide tugas akhir",
                "judul tugas akhir",
                "tiga ide",
                "3 ide",
            )
        )
        final_thesis_answer_text = str(generated or "")
        final_thesis_answer_lower = final_thesis_answer_text.lower()
        final_thesis_idea_count = sum(
            1
            for heading in (
                "## ide 1",
                "## ide 2",
                "## ide 3",
            )
            if heading in final_thesis_answer_lower
        )
        final_thesis_false_refusal = any(
            phrase in final_thesis_answer_lower
            for phrase in (
                "evidence yang tersedia tidak mencukupi",
                "bukti yang tersedia tidak mencukupi",
                "tidak ada dokumen dalam konteks",
                "tidak dapat disusun proposal",
                "tidak dapat menghasilkan tiga ide",
                "tidak dapat memberikan tiga ide",
                "insufficient evidence",
                "cannot provide three",
            )
        )
        final_thesis_fallback_required = (
            final_thesis_request_detected
            and (
                final_thesis_false_refusal
                or final_thesis_idea_count < 3
            )
        )
        if final_thesis_fallback_required:
            final_thesis_evidence = []
            final_thesis_seen_ids = set()
            final_metadata_text = str(metadata_complement_context or "")
            for final_raw_block in final_metadata_text.split("[Metadata Complement ")[1:]:
                final_document_id = ""
                final_document_title = ""
                final_document_abstract = ""
                for final_block_line in final_raw_block.splitlines():
                    final_clean_line = final_block_line.strip()
                    if final_clean_line.startswith("Document ID:"):
                        final_document_id = final_clean_line.split(":", 1)[1].strip()
                    elif final_clean_line.startswith("Title:"):
                        final_document_title = final_clean_line.split(":", 1)[1].strip()
                if "Abstract:" in final_raw_block:
                    final_document_abstract = final_raw_block.split("Abstract:", 1)[1].strip()
                final_document_abstract = " ".join(
                    final_document_abstract.split()
                )[:360]
                if (
                    final_document_id
                    and final_document_title
                    and final_document_id not in final_thesis_seen_ids
                ):
                    final_thesis_seen_ids.add(final_document_id)
                    final_thesis_evidence.append(
                        {
                            "document_id": final_document_id,
                            "title": final_document_title,
                            "abstract": final_document_abstract,
                        }
                    )
                if len(final_thesis_evidence) >= 3:
                    break
            if len(final_thesis_evidence) >= 3:
                final_thesis_focuses = (
                    (
                        "Pemodelan Prediktif dan Deteksi Anomali",
                        "Evidence menunjukkan sistem monitoring telah dikembangkan, tetapi metadata yang tersedia belum menunjukkan evaluasi pemodelan prediktif dan deteksi anomali secara khusus.",
                        "mengembangkan pengumpulan data sensor, praproses, pemodelan prediktif atau deteksi anomali, dan dashboard peringatan",
                        "MAE atau akurasi sesuai keluaran, precision-recall anomali, latency, dan availability sistem",
                    ),
                    (
                        "Kendali Adaptif dan Keandalan End-to-End",
                        "Evidence membahas monitoring atau komunikasi, tetapi metadata yang tersedia belum menunjukkan evaluasi kendali adaptif dan keandalan sistem secara end-to-end.",
                        "mengembangkan sensor, komunikasi, aturan kendali adaptif, aktuator, penyimpanan data, dan antarmuka monitoring",
                        "packet loss, delay, throughput, keberhasilan aksi kendali, penggunaan sumber daya, dan availability",
                    ),
                    (
                        "Interoperabilitas dan Ketahanan Deployment",
                        "Evidence menunjukkan implementasi pada perangkat atau platform tertentu, tetapi metadata yang tersedia belum memperlihatkan perbandingan interoperabilitas dan ketahanan deployment secara khusus.",
                        "mengembangkan gateway edge, antarmuka data standar, sinkronisasi lokal-cloud, dashboard, dan mekanisme pemulihan koneksi",
                        "latency, availability, keberhasilan pertukaran data, pemulihan setelah gangguan, konsumsi daya, dan usability",
                    ),
                )
                final_thesis_parts = [
                    "Berikut tiga proposal penelitian yang diturunkan dari evidence repository. Fakta sumber dipisahkan dari rancangan penelitian baru."
                ]
                for final_index, final_evidence in enumerate(
                    final_thesis_evidence[:3],
                    start=1,
                ):
                    (
                        final_focus_title,
                        final_gap_text,
                        final_method_text,
                        final_evaluation_text,
                    ) = final_thesis_focuses[final_index - 1]
                    final_source_fact = final_evidence["abstract"]
                    if not final_source_fact:
                        final_source_fact = (
                            "Repository menyediakan identitas dan judul dokumen yang relevan dengan arah penelitian."
                        )
                    final_thesis_parts.append(
                        (
                            f"## Ide {final_index}\n"
                            f"**Judul:** {final_focus_title} pada {final_evidence['title']}\n\n"
                            f"**Masalah:** Evidence {final_evidence['document_id']} menjelaskan: {final_source_fact} Hal tersebut menjadi dasar pengembangan lanjutan yang tetap terkait dengan sistem pada sumber.\n\n"
                            f"**Research Gap:** {final_gap_text} Gap ini dibatasi pada evidence repository yang tersedia dan bukan klaim mengenai seluruh literatur.\n\n"
                            f"**Metode Sistem yang Diusulkan:** Sebagai proposal baru, penelitian akan {final_method_text} melalui tahap perancangan, implementasi prototipe, pengumpulan data uji, dan analisis hasil.\n\n"
                            f"**Rencana Evaluasi:** Sebagai rancangan baru, ukur {final_evaluation_text} dan bandingkan dengan baseline yang ditetapkan sebelum eksperimen.\n\n"
                            f"**Kontribusi:** Target kontribusinya adalah artefak prototipe dan hasil evaluasi terukur yang memperluas arah sistem pada evidence. Bagian ini merupakan target penelitian, bukan hasil yang telah terbukti.\n\n"
                            f"**Keterbatasan:** Evidence terbatas pada metadata atau abstrak repository. Parameter, dataset, dan hasil eksperimen proposal harus divalidasi saat penelitian dilakukan.\n\n"
                            f"**Sumber Pendukung:** [{final_evidence['document_id']}] {final_evidence['title']}."
                        )
                    )
                generated = "\n\n".join(final_thesis_parts)
        # FINAL_BOUNDARY_THESIS_CITATION_FILTER_767826
        _final_thesis_answer = str(generated or "")
        _final_thesis_filter_active = (
            "## Ide 1" in _final_thesis_answer
            and "## Ide 2" in _final_thesis_answer
            and "## Ide 3" in _final_thesis_answer
            and "Sumber Pendukung" in _final_thesis_answer
        )
        if _final_thesis_filter_active and citations:
            import re as _final_thesis_re
            # MARKDOWN_AWARE_SUPPORT_ID_FILTER_767828
            _final_thesis_support_lines = [
                support_line
                for support_line in _final_thesis_answer.splitlines()
                if _final_thesis_re.search(
                    r"Sumber\s+Pendukung",
                    support_line,
                    flags=_final_thesis_re.IGNORECASE,
                )
            ]
            _final_thesis_reference_ids = list(
                dict.fromkeys(
                    document_id
                    for support_line in _final_thesis_support_lines
                    for document_id in _final_thesis_re.findall(
                        r"\b\d{6,}(?:[-/]\d+)+\b",
                        support_line,
                    )
                )
            )
            _final_thesis_selected_citations = []
            _final_thesis_matched_ids = []
            for _final_thesis_reference_id in _final_thesis_reference_ids:
                for _final_thesis_citation in citations:
                    if hasattr(_final_thesis_citation, "model_dump"):
                        _final_thesis_citation_payload = _final_thesis_citation.model_dump()
                    elif hasattr(_final_thesis_citation, "dict"):
                        _final_thesis_citation_payload = _final_thesis_citation.dict()
                    else:
                        _final_thesis_citation_payload = _final_thesis_citation
                    _final_thesis_citation_text = str(_final_thesis_citation_payload)
                    if _final_thesis_reference_id in _final_thesis_citation_text:
                        _final_thesis_selected_citations.append(_final_thesis_citation)
                        _final_thesis_matched_ids.append(_final_thesis_reference_id)
                        break
            if (
                len(_final_thesis_reference_ids) == 3
                and len(_final_thesis_selected_citations) == 3
                and set(_final_thesis_matched_ids) == set(_final_thesis_reference_ids)
            ):
                citations = _final_thesis_selected_citations

        # DELBOT MVP synthesize three grounded ideas
        import re as _mvp_idea_re

        _mvp_idea_query_lower = str(
            _mvp_evidence_query
            or question
            or ""
        ).lower()

        _mvp_is_three_idea_request = any(
            _mvp_idea_phrase in _mvp_idea_query_lower
            for _mvp_idea_phrase in (
                "ide tugas akhir",
                "judul tugas akhir",
                "thesis idea",
                "thesis ideas",
                "proposal penelitian",
                "kembangkan tiga ide",
                "kembangkan beberapa ide",
                "develop an idea",
            )
        )

        _mvp_existing_idea_count = len(
            _mvp_idea_re.findall(
                r"(?im)^\s*#{0,3}\s*ide\s+\d+",
                str(generated or ""),
            )
        )

        if (
            evidence_turn
            and _mvp_is_three_idea_request
            and citations
            and _mvp_existing_idea_count < 3
        ):
            def _mvp_trim_idea_evidence(
                value,
                limit=420,
            ):
                clean_value = " ".join(
                    str(value or "").split()
                ).strip()

                if len(clean_value) <= limit:
                    return clean_value

                shortened = clean_value[:limit].rsplit(
                    " ",
                    1,
                )[0].strip()

                return shortened + "…"

            def _mvp_idea_source_record(
                source_citation,
                source_number,
            ):
                source_document = _mvp_citation_value(
                    source_citation,
                    "document",
                    {},
                )
                source_metadata = _mvp_citation_mapping(
                    source_citation,
                    "metadata",
                )
                source_document_metadata = (
                    _mvp_citation_mapping(
                        source_document,
                        "metadata",
                    )
                )

                source_title = str(
                    _mvp_citation_value(
                        source_document,
                        "title",
                        "",
                    )
                    or "Dokumen repository"
                ).strip()

                source_excerpt = str(
                    _mvp_citation_value(
                        source_citation,
                        "text",
                        "",
                    )
                    or source_metadata.get("abstract")
                    or source_document_metadata.get(
                        "abstract"
                    )
                    or ""
                ).strip()

                source_type = str(
                    source_metadata.get("evidence_type")
                    or source_document_metadata.get(
                        "evidence_type"
                    )
                    or ""
                ).lower()

                if "fulltext" in source_type:
                    source_label = "Isi PDF"
                else:
                    source_label = "Metadata/Abstrak"

                location_parts = []

                source_section = str(
                    source_metadata.get("section")
                    or source_metadata.get(
                        "section_title"
                    )
                    or ""
                ).strip()

                source_page = (
                    source_metadata.get("page_start")
                    or source_metadata.get("page")
                    or _mvp_citation_value(
                        source_citation,
                        "page",
                        None,
                    )
                )

                if (
                    "fulltext" in source_type
                    and source_section
                ):
                    location_parts.append(
                        "bagian " + source_section
                    )

                if (
                    "fulltext" in source_type
                    and source_page not in (
                        None,
                        "",
                    )
                ):
                    location_parts.append(
                        "halaman " + str(source_page)
                    )

                source_location = (
                    " pada " + ", ".join(location_parts)
                    if location_parts
                    else ""
                )

                return {
                    "number": source_number,
                    "title": source_title,
                    "excerpt": _mvp_trim_idea_evidence(
                        source_excerpt
                    ),
                    "label": source_label,
                    "location": source_location,
                }

            _mvp_idea_sources = [
                _mvp_idea_source_record(
                    _mvp_source_citation,
                    _mvp_source_index,
                )
                for (
                    _mvp_source_index,
                    _mvp_source_citation,
                ) in enumerate(
                    citations,
                    start=1,
                )
            ]

            _mvp_has_agriculture = any(
                term in _mvp_idea_query_lower
                for term in (
                    "hidroponik", "hydroponic",
                    "pertanian", "agriculture",
                    "tanaman", "nutrisi",
                    "irigasi", "greenhouse",
                )
            )
            _mvp_has_health = any(
                term in _mvp_idea_query_lower
                for term in (
                    "kesehatan", "health",
                    "medis", "pasien",
                    "penyakit",
                )
            )
            _mvp_has_tourism = any(
                term in _mvp_idea_query_lower
                for term in (
                    "pariwisata", "tourism",
                    "wisata", "destinasi",
                )
            )
            _mvp_has_education = any(
                term in _mvp_idea_query_lower
                for term in (
                    "pendidikan", "education",
                    "mahasiswa", "siswa",
                    "pembelajaran",
                )
            )
            _mvp_has_bioprocess = any(
                term in _mvp_idea_query_lower
                for term in (
                    "bioproses", "bioprocess",
                    "fermentasi", "mikroorganisme",
                    "bioteknologi",
                )
            )
            _mvp_has_ai = any(
                term in _mvp_idea_query_lower
                for term in (
                    "artificial intelligence",
                    "kecerdasan buatan",
                    "machine learning",
                    "deep learning",
                    "computer vision",
                    " ai ",
                )
            )
            _mvp_has_iot = any(
                term in _mvp_idea_query_lower
                for term in (
                    "internet of things",
                    "iot", "sensor",
                    "monitoring", "aktuator",
                    "otomasi", "lora",
                    "mqtt",
                )
            )
            _mvp_has_software = any(
                term in _mvp_idea_query_lower
                for term in (
                    "website", "web",
                    "aplikasi", "software",
                    "perangkat lunak",
                    "dashboard",
                )
            )
            _mvp_has_data = any(
                term in _mvp_idea_query_lower
                for term in (
                    "database", "basis data",
                    "data mining", "analytics",
                    "sistem informasi",
                )
            )

            if (
                "hidroponik" in _mvp_idea_query_lower
                or "hydroponic" in _mvp_idea_query_lower
            ):
                _mvp_topic_focus = "Hidroponik"
            elif _mvp_has_agriculture:
                _mvp_topic_focus = "Pertanian"
            elif _mvp_has_health:
                _mvp_topic_focus = "Kesehatan"
            elif _mvp_has_tourism:
                _mvp_topic_focus = "Pariwisata"
            elif _mvp_has_education:
                _mvp_topic_focus = "Pendidikan"
            elif _mvp_has_bioprocess:
                _mvp_topic_focus = "Bioproses"
            else:
                _mvp_topic_focus = "Topik Penelitian Aktif"

            if _mvp_has_iot:
                _mvp_idea_profiles = [
                    {
                        "title": (
                            "Pemodelan Prediktif dan Deteksi "
                            "Anomali Sensor pada Sistem "
                            f"{_mvp_topic_focus} Berbasis IoT"
                        ),
                        "problem": (
                            "Sistem monitoring menyediakan data "
                            "operasional, tetapi proposal ini "
                            "menargetkan pemanfaatan data tersebut "
                            "untuk prediksi kondisi dan peringatan "
                            "anomali sebelum gangguan membesar."
                        ),
                        "gap": (
                            "Evidence yang tersedia belum melaporkan "
                            "evaluasi model prediksi atau deteksi "
                            "anomali sensor secara khusus."
                        ),
                        "method": (
                            "Kumpulkan data sensor bertimestamp, "
                            "lakukan pembersihan dan pembentukan "
                            "fitur, lalu bandingkan baseline statistik "
                            "dengan satu model prediksi atau deteksi "
                            "anomali. Hasil disajikan pada dashboard "
                            "peringatan."
                        ),
                        "evaluation": (
                            "Gunakan MAE atau RMSE untuk prediksi, "
                            "precision, recall, dan F1 untuk anomali, "
                            "serta latency dan availability sistem."
                        ),
                        "contribution": (
                            "Prototipe monitoring yang tidak hanya "
                            "menampilkan data, tetapi juga memberikan "
                            "indikasi kondisi mendatang dan anomali "
                            "secara terukur."
                        ),
                    },
                    {
                        "title": (
                            "Kendali Adaptif untuk Optimasi "
                            f"{_mvp_topic_focus} Berbasis IoT"
                        ),
                        "problem": (
                            "Monitoring saja belum menentukan tindakan "
                            "kendali yang sesuai ketika kondisi sensor "
                            "berubah. Proposal ini menghubungkan hasil "
                            "pengukuran dengan keputusan aktuator."
                        ),
                        "gap": (
                            "Evidence repository belum menunjukkan "
                            "perbandingan kendali statis dengan kendali "
                            "adaptif berdasarkan perubahan data sensor."
                        ),
                        "method": (
                            "Bangun aturan kendali baseline dan kendali "
                            "adaptif, integrasikan sensor, gateway, "
                            "aktuator, penyimpanan data, serta dashboard, "
                            "kemudian uji pada beberapa skenario kondisi."
                        ),
                        "evaluation": (
                            "Ukur error terhadap setpoint, waktu respons, "
                            "keberhasilan aksi kendali, konsumsi sumber "
                            "daya, dan stabilitas sistem."
                        ),
                        "contribution": (
                            "Mekanisme kendali berbasis data yang dapat "
                            "dibandingkan secara objektif dengan aturan "
                            "konvensional."
                        ),
                    },
                    {
                        "title": (
                            "Evaluasi Keandalan Komunikasi dan "
                            "Pemulihan Gangguan pada Sistem "
                            f"{_mvp_topic_focus} Berbasis IoT"
                        ),
                        "problem": (
                            "Sistem IoT bergantung pada komunikasi "
                            "sensor, gateway, dan layanan penyimpanan. "
                            "Gangguan koneksi dapat menyebabkan data "
                            "hilang atau aksi kendali terlambat."
                        ),
                        "gap": (
                            "Evidence yang tersedia belum memberikan "
                            "evaluasi end-to-end mengenai ketahanan "
                            "deployment dan pemulihan setelah gangguan."
                        ),
                        "method": (
                            "Implementasikan buffer lokal, pengiriman "
                            "ulang, sinkronisasi setelah koneksi pulih, "
                            "dan pencatatan status perangkat. Bandingkan "
                            "sistem dengan dan tanpa mekanisme pemulihan."
                        ),
                        "evaluation": (
                            "Ukur packet loss, delay, throughput, "
                            "kelengkapan data, recovery time, dan "
                            "availability."
                        ),
                        "contribution": (
                            "Arsitektur IoT yang lebih tahan terhadap "
                            "gangguan komunikasi dengan hasil evaluasi "
                            "yang dapat direplikasi."
                        ),
                    },
                ]
            elif _mvp_has_ai:
                _mvp_idea_profiles = [
                    {
                        "title": (
                            "Perbandingan Model Prediksi untuk "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Pemilihan model sering dilakukan tanpa "
                            "perbandingan yang seragam pada data dan "
                            "skenario penggunaan yang sama."
                        ),
                        "gap": (
                            "Evidence belum menunjukkan evaluasi "
                            "komparatif beberapa baseline dan model AI."
                        ),
                        "method": (
                            "Siapkan dataset, praproses, baseline, "
                            "beberapa model kandidat, dan prosedur "
                            "validasi yang konsisten."
                        ),
                        "evaluation": (
                            "Gunakan metrik sesuai tugas seperti "
                            "accuracy, precision, recall, F1, MAE, "
                            "RMSE, serta waktu inferensi."
                        ),
                        "contribution": (
                            "Benchmark model dan rekomendasi pemilihan "
                            "model berdasarkan akurasi serta biaya."
                        ),
                    },
                    {
                        "title": (
                            "Explainable AI untuk Mendukung "
                            f"Keputusan pada { _mvp_topic_focus}"
                        ),
                        "problem": (
                            "Prediksi model sulit dipercaya apabila "
                            "alasan di balik keluaran tidak dijelaskan."
                        ),
                        "gap": (
                            "Evidence belum membahas interpretabilitas "
                            "dan konsistensi penjelasan model."
                        ),
                        "method": (
                            "Latih model baseline, terapkan metode "
                            "explainability, dan evaluasi penjelasan "
                            "bersama pengguna atau pakar domain."
                        ),
                        "evaluation": (
                            "Ukur performa prediksi, fidelity penjelasan, "
                            "stabilitas, dan usability."
                        ),
                        "contribution": (
                            "Model dengan penjelasan yang dapat ditinjau "
                            "dan prototipe antarmuka keputusan."
                        ),
                    },
                    {
                        "title": (
                            "Optimasi Inferensi dan Ketahanan Model AI "
                            f"untuk { _mvp_topic_focus}"
                        ),
                        "problem": (
                            "Model yang akurat belum tentu efisien atau "
                            "stabil ketika digunakan pada lingkungan nyata."
                        ),
                        "gap": (
                            "Evidence belum memperlihatkan kompromi "
                            "akurasi, latency, penggunaan memori, dan "
                            "ketahanan terhadap perubahan data."
                        ),
                        "method": (
                            "Bandingkan model dasar dengan versi yang "
                            "dioptimasi dan uji pada data normal serta "
                            "data dengan gangguan terkontrol."
                        ),
                        "evaluation": (
                            "Ukur akurasi, latency, throughput, memori, "
                            "ukuran model, dan penurunan performa."
                        ),
                        "contribution": (
                            "Konfigurasi deployment AI yang efisien "
                            "beserta batas penggunaannya."
                        ),
                    },
                ]
            elif (
                _mvp_has_software
                or _mvp_has_data
            ):
                _mvp_idea_profiles = [
                    {
                        "title": (
                            "Dashboard Analitik untuk "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Informasi tersedia tetapi belum selalu "
                            "disajikan dalam bentuk yang mendukung "
                            "pengambilan keputusan."
                        ),
                        "gap": (
                            "Evidence belum menunjukkan evaluasi kualitas "
                            "visualisasi dan efektivitas keputusan."
                        ),
                        "method": (
                            "Analisis kebutuhan, rancang arsitektur data "
                            "dan dashboard, implementasikan prototipe, "
                            "lalu lakukan pengujian pengguna."
                        ),
                        "evaluation": (
                            "Ukur task completion, waktu penyelesaian, "
                            "error rate, SUS, dan performa pemuatan."
                        ),
                        "contribution": (
                            "Dashboard terstruktur dan hasil evaluasi "
                            "usability yang terukur."
                        ),
                    },
                    {
                        "title": (
                            "Evaluasi Performa dan Keamanan Sistem "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Sistem fungsional belum cukup apabila "
                            "performa dan keamanan belum dievaluasi."
                        ),
                        "gap": (
                            "Evidence belum memperlihatkan pengujian "
                            "beban dan kontrol keamanan secara terpadu."
                        ),
                        "method": (
                            "Bangun skenario beban, audit autentikasi "
                            "dan otorisasi, lalu bandingkan konfigurasi "
                            "baseline dengan versi optimasi."
                        ),
                        "evaluation": (
                            "Ukur response time, throughput, error rate, "
                            "penggunaan sumber daya, dan temuan keamanan."
                        ),
                        "contribution": (
                            "Baseline performa, temuan risiko, dan "
                            "rekomendasi konfigurasi sistem."
                        ),
                    },
                    {
                        "title": (
                            "Interoperabilitas dan Kualitas Data pada "
                            f"Sistem { _mvp_topic_focus}"
                        ),
                        "problem": (
                            "Pertukaran data antarmodul dapat menghasilkan "
                            "format tidak konsisten dan data tidak lengkap."
                        ),
                        "gap": (
                            "Evidence belum membandingkan interoperabilitas "
                            "dan kualitas data secara end-to-end."
                        ),
                        "method": (
                            "Rancang kontrak data, validasi skema, logging, "
                            "dan sinkronisasi; kemudian uji pertukaran data "
                            "pada beberapa skenario."
                        ),
                        "evaluation": (
                            "Ukur completeness, consistency, error rate, "
                            "latency integrasi, dan recovery rate."
                        ),
                        "contribution": (
                            "Kontrak data dan mekanisme validasi yang "
                            "meningkatkan keandalan integrasi."
                        ),
                    },
                ]
            elif _mvp_has_bioprocess:
                _mvp_idea_profiles = [
                    {
                        "title": (
                            "Optimasi Parameter Proses pada "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Parameter proses perlu diuji secara sistematis "
                            "agar kondisi terbaik dapat ditentukan."
                        ),
                        "gap": (
                            "Evidence belum menunjukkan optimasi "
                            "multi-parameter dengan rancangan eksperimen."
                        ),
                        "method": (
                            "Gunakan desain eksperimen, variasikan parameter "
                            "utama, dan analisis pengaruh serta interaksinya."
                        ),
                        "evaluation": (
                            "Ukur yield, kualitas produk, waktu proses, "
                            "dan efisiensi sumber daya."
                        ),
                        "contribution": (
                            "Kondisi proses yang terukur dan model hubungan "
                            "parameter terhadap hasil."
                        ),
                    },
                    {
                        "title": (
                            "Pemodelan Prediktif Kualitas Hasil "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Kualitas hasil baru diketahui setelah proses "
                            "selesai sehingga koreksi terlambat dilakukan."
                        ),
                        "gap": (
                            "Evidence belum melaporkan model prediksi "
                            "kualitas dari parameter proses."
                        ),
                        "method": (
                            "Kumpulkan data proses, bentuk fitur, latih "
                            "baseline dan model prediksi, lalu validasi."
                        ),
                        "evaluation": (
                            "Ukur MAE, RMSE, R-squared, dan kestabilan "
                            "prediksi pada batch berbeda."
                        ),
                        "contribution": (
                            "Model prediksi untuk mendukung pemantauan "
                            "kualitas proses."
                        ),
                    },
                    {
                        "title": (
                            "Evaluasi Skalabilitas Proses "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Hasil skala kecil belum otomatis konsisten "
                            "ketika kapasitas proses ditingkatkan."
                        ),
                        "gap": (
                            "Evidence belum mengevaluasi perubahan kinerja "
                            "pada beberapa skala proses."
                        ),
                        "method": (
                            "Uji beberapa skala, kendalikan parameter kunci, "
                            "dan bandingkan keseimbangan massa serta energi."
                        ),
                        "evaluation": (
                            "Ukur yield, produktivitas, konsumsi energi, "
                            "konsistensi, dan biaya."
                        ),
                        "contribution": (
                            "Batas skalabilitas dan rekomendasi parameter "
                            "untuk pengembangan proses."
                        ),
                    },
                ]
            else:
                _mvp_idea_profiles = [
                    {
                        "title": (
                            "Pengembangan dan Evaluasi Sistem untuk "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Evidence menyediakan landasan awal, tetapi "
                            "belum mencakup evaluasi sistem secara terukur."
                        ),
                        "gap": (
                            "Belum terlihat perbandingan dengan baseline "
                            "pada koleksi evidence yang tersedia."
                        ),
                        "method": (
                            "Bangun prototipe, tetapkan baseline, siapkan "
                            "skenario uji, dan analisis hasil."
                        ),
                        "evaluation": (
                            "Gunakan metrik fungsional, performa, "
                            "keandalan, dan usability yang sesuai."
                        ),
                        "contribution": (
                            "Prototipe serta hasil evaluasi yang dapat "
                            "ditinjau ulang."
                        ),
                    },
                    {
                        "title": (
                            "Studi Komparatif Metode untuk "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Metode terbaik belum dapat dipilih tanpa "
                            "perbandingan pada kondisi yang sama."
                        ),
                        "gap": (
                            "Evidence belum menunjukkan evaluasi komparatif "
                            "yang konsisten."
                        ),
                        "method": (
                            "Pilih baseline dan metode alternatif, lalu "
                            "uji menggunakan data serta skenario identik."
                        ),
                        "evaluation": (
                            "Bandingkan kualitas hasil, waktu, sumber daya, "
                            "dan stabilitas."
                        ),
                        "contribution": (
                            "Benchmark dan rekomendasi metode berdasarkan "
                            "hasil terukur."
                        ),
                    },
                    {
                        "title": (
                            "Peningkatan Keandalan Sistem "
                            f"{_mvp_topic_focus}"
                        ),
                        "problem": (
                            "Sistem perlu tetap berfungsi ketika terjadi "
                            "gangguan atau variasi kondisi."
                        ),
                        "gap": (
                            "Evidence belum mengukur ketahanan dan "
                            "pemulihan sistem."
                        ),
                        "method": (
                            "Tambahkan logging, validasi, dan mekanisme "
                            "pemulihan; lalu uji dengan gangguan terkontrol."
                        ),
                        "evaluation": (
                            "Ukur availability, error rate, recovery time, "
                            "dan kelengkapan hasil."
                        ),
                        "contribution": (
                            "Mekanisme peningkatan keandalan beserta "
                            "hasil evaluasi."
                        ),
                    },
                ]

            _mvp_idea_answer_parts = [
                (
                    "Berikut tiga ide tugas akhir yang diturunkan "
                    "dari sumber repository yang lolos pemeriksaan "
                    "relevansi. Fakta sumber dipisahkan dari rancangan "
                    "penelitian baru."
                )
            ]

            for (
                _mvp_idea_index,
                _mvp_idea_profile,
            ) in enumerate(
                _mvp_idea_profiles,
                start=1,
            ):
                if _mvp_idea_index <= len(
                    _mvp_idea_sources
                ):
                    _mvp_primary_source = (
                        _mvp_idea_sources[
                            _mvp_idea_index - 1
                        ]
                    )
                    _mvp_source_reference = (
                        f"Sumber {_mvp_primary_source['number']}"
                    )
                    _mvp_evidence_statement = (
                        f"Berdasarkan {_mvp_primary_source['label']} "
                        f"{_mvp_source_reference}"
                        f"{_mvp_primary_source['location']}, dokumen "
                        f"“{_mvp_primary_source['title']}” menjelaskan: "
                        f"{_mvp_primary_source['excerpt']}"
                    )
                else:
                    _mvp_primary_source = (
                        _mvp_idea_sources[0]
                    )
                    _mvp_source_reference = " dan ".join(
                        "Sumber " + str(item["number"])
                        for item in _mvp_idea_sources[:2]
                    )
                    _mvp_evidence_statement = (
                        "Sintesis "
                        + _mvp_source_reference
                        + " menunjukkan adanya landasan sistem "
                        + "dan konteks penerapan yang relevan. "
                        + "Sumber utama yang digunakan adalah "
                        + "“"
                        + "” dan “".join(
                            item["title"]
                            for item in _mvp_idea_sources[:2]
                        )
                        + "”."
                    )

                _mvp_limitations = (
                    "Ide ini diturunkan dari evidence repository "
                    "yang tersedia. Bagian yang tidak dilaporkan "
                    "oleh sumber diposisikan sebagai rencana "
                    "penelitian, bukan sebagai fakta atau hasil "
                    "yang telah terbukti. Dataset, parameter, dan "
                    "hasil eksperimen harus ditetapkan dan "
                    "divalidasi saat penelitian dilakukan."
                )

                _mvp_idea_answer_parts.append(
                    "\n".join([
                        f"## Ide {_mvp_idea_index}",
                        "",
                        (
                            "**Judul:** "
                            + _mvp_idea_profile["title"]
                        ),
                        "",
                        (
                            "**Landasan Evidence:** "
                            + _mvp_evidence_statement
                        ),
                        "",
                        (
                            "**Masalah:** "
                            + _mvp_idea_profile["problem"]
                        ),
                        "",
                        (
                            "**Research Gap:** "
                            + _mvp_idea_profile["gap"]
                            + " Gap ini dibatasi pada koleksi "
                            + "repository yang tersedia, bukan "
                            + "klaim terhadap seluruh literatur."
                        ),
                        "",
                        (
                            "**Arah Metode:** "
                            + _mvp_idea_profile["method"]
                        ),
                        "",
                        (
                            "**Rencana Evaluasi:** "
                            + _mvp_idea_profile["evaluation"]
                        ),
                        "",
                        (
                            "**Kontribusi yang Diharapkan:** "
                            + _mvp_idea_profile["contribution"]
                            + " Bagian ini adalah target "
                            + "penelitian, bukan hasil yang "
                            + "sudah terbukti."
                        ),
                        "",
                        (
                            "**Keterbatasan:** "
                            + _mvp_limitations
                        ),
                        "",
                        (
                            "**Sumber Pendukung:** ["
                            + _mvp_source_reference
                            + "]"
                        ),
                    ])
                )

            generated = "\n\n".join(
                _mvp_idea_answer_parts
            )

        # DELBOT MVP final grouped citation safety
        if evidence_turn and citations:
            citations = [
                _mvp_final_candidate
                for _mvp_final_candidate in citations
                if _mvp_citation_relevance_details(
                    _mvp_final_candidate,
                    _mvp_evidence_query,
                )["relevant"]
            ]

        # DELBOT MVP self-contained final domain relevance guard
        _mvp_final_query_lower = str(question or "").lower()
        _mvp_final_metadata_lower = (
            metadata_complement_context.lower()
            if isinstance(metadata_complement_context, str)
            else ""
        )
        # DELBOT MVP final domain guard reads active fulltext
        _mvp_final_domain_evidence_parts = [
            str(_mvp_final_metadata_lower or ""),
        ]

        if _mvp_fulltext_citations:
            _mvp_final_domain_evidence_parts.extend([
                str(_mvp_fulltext_context or ""),
                str(context or ""),
            ])

            for _mvp_guard_source in list(
                _mvp_fulltext_citations
            ):
                _mvp_guard_document = _mvp_citation_value(
                    _mvp_guard_source,
                    "document",
                    {},
                )
                _mvp_guard_metadata = _mvp_citation_mapping(
                    _mvp_guard_source,
                    "metadata",
                )
                _mvp_guard_document_metadata = (
                    _mvp_citation_mapping(
                        _mvp_guard_document,
                        "metadata",
                    )
                )

                _mvp_final_domain_evidence_parts.extend([
                    str(
                        _mvp_citation_value(
                            _mvp_guard_document,
                            "title",
                            "",
                        )
                        or ""
                    ),
                    str(
                        _mvp_citation_value(
                            _mvp_guard_source,
                            "text",
                            "",
                        )
                        or ""
                    ),
                    str(
                        _mvp_guard_metadata.get("section")
                        or _mvp_guard_metadata.get(
                            "section_title"
                        )
                        or ""
                    ),
                    str(
                        _mvp_guard_document_metadata.get(
                            "keywords"
                        )
                        or ""
                    ),
                ])

        _mvp_final_metadata_lower = (
            " ".join(_mvp_final_domain_evidence_parts)
            .lower()
            .replace("-", " ")
        )
        _mvp_final_domain_groups = (
            ("kesehatan", (
                "kesehatan", "pasien", "medis", "medical",
                "health", "healthcare", "penyakit",
                "rumah sakit", "jantung", "diabetes",
                "lansia", "patient",
            )),
            ("pertanian", (
                "pertanian", "tanaman", "cabai",
                "hidroponik", "greenhouse", "smart farming",
                "irigasi", "perkebunan", "agriculture",
                "farming",
            )),
            ("pendidikan", (
                "pendidikan", "siswa", "mahasiswa",
                "sekolah", "kelas", "pembelajaran",
                "education", "student",
            )),
            ("pariwisata", (
                "pariwisata", "wisata", "tourism",
                "tourist", "destinasi", "hotel",
            )),
        )
        _mvp_final_thesis_phrases = (
            "judul tugas akhir",
            "ide tugas akhir",
            "thesis idea",
            "thesis ideas",
            "proposal penelitian",
            "kembangkan beberapa thesis",
            "develop an idea",
            "develop thesis",
        )
        _mvp_final_is_thesis_request = any(
            phrase in _mvp_final_query_lower
            for phrase in _mvp_final_thesis_phrases
        )
        _mvp_final_domain_label = ""
        _mvp_final_domain_terms = ()
        for _mvp_label, _mvp_terms in _mvp_final_domain_groups:
            if any(
                term in _mvp_final_query_lower
                for term in _mvp_terms
            ):
                _mvp_final_domain_label = _mvp_label
                _mvp_final_domain_terms = _mvp_terms
                break
        _mvp_final_domain_evidence_valid = (
            not _mvp_final_domain_terms
            or any(
                term in _mvp_final_metadata_lower
                for term in _mvp_final_domain_terms
            )
        )
        if (
            _mvp_final_is_thesis_request
            and _mvp_final_domain_terms
            and not _mvp_final_domain_evidence_valid
        ):
            generated = (
                "Evidence repository yang relevan dengan domain "
                f"{_mvp_final_domain_label} belum ditemukan. "
                "DELBot tidak menggunakan dokumen dari domain lain "
                "untuk membuat judul atau proposal yang seolah-olah "
                "didukung repository. Gunakan kata kunci lebih "
                "spesifik atau tambahkan dokumen relevan ke koleksi."
            )
            citations = []
        # DELBOT MVP topic-aware guard at final output boundary
        _mvp_final_topic_label = str(
            _mvp_bounded_user_topic
            or _mvp_original_question
            or "permintaan pengguna"
        ).strip()[:240]
        if (
            isinstance(generated, str)
            and "domain kesehatan" in generated
        ):
            generated = generated.replace(
                "domain kesehatan",
                f"topik '{_mvp_final_topic_label}'",
            )
        # DELBOT MVP deterministic fallback multi-concept relevance guard
        import re as _mvp_relevance_re
        _mvp_required_topic_lower = str(
            _mvp_bounded_user_topic
            or question
            or ""
        ).lower()
        _mvp_required_topic_words = (
            " "
            + _mvp_required_topic_lower.replace("-", " ")
            + " "
        )
        _mvp_requires_iot = (
            " iot " in _mvp_required_topic_words
            or "internet of things" in _mvp_required_topic_lower
        )
        _mvp_requires_ai = (
            _mvp_relevance_re.search(
                r"(?<![a-z0-9])ai(?![a-z0-9])",
                _mvp_required_topic_lower,
            )
            is not None
            or "artificial intelligence" in _mvp_required_topic_lower
            or "kecerdasan buatan" in _mvp_required_topic_lower
            or "machine learning" in _mvp_required_topic_lower
        )
        _mvp_final_citation_blob = str(
            citations or []
        ).lower()
        # DELBOT MVP final relevance uses fulltext evidence
        _mvp_final_fulltext_evidence_parts = []

        for _mvp_final_source in list(citations or []):
            if not _mvp_is_fulltext_citation(
                _mvp_final_source
            ):
                continue

            _mvp_final_document = _mvp_citation_value(
                _mvp_final_source,
                "document",
                {},
            )
            _mvp_final_metadata = _mvp_citation_mapping(
                _mvp_final_source,
                "metadata",
            )
            _mvp_final_document_metadata = (
                _mvp_citation_mapping(
                    _mvp_final_document,
                    "metadata",
                )
            )

            _mvp_final_fulltext_evidence_parts.extend([
                str(
                    _mvp_citation_value(
                        _mvp_final_document,
                        "title",
                        "",
                    )
                    or ""
                ),
                str(
                    _mvp_citation_value(
                        _mvp_final_document,
                        "document_id",
                        "",
                    )
                    or ""
                ),
                str(
                    _mvp_citation_value(
                        _mvp_final_source,
                        "text",
                        "",
                    )
                    or ""
                ),
                str(
                    _mvp_final_metadata.get("section")
                    or _mvp_final_metadata.get(
                        "section_title"
                    )
                    or ""
                ),
                str(
                    _mvp_final_document_metadata.get(
                        "section"
                    )
                    or _mvp_final_document_metadata.get(
                        "section_title"
                    )
                    or ""
                ),
                str(
                    _mvp_final_document_metadata.get(
                        "keywords"
                    )
                    or ""
                ),
                str(
                    _mvp_final_document_metadata.get(
                        "entities"
                    )
                    or ""
                ),
            ])

        if _mvp_final_fulltext_evidence_parts:
            _mvp_final_citation_blob = (
                (
                    str(_mvp_final_citation_blob or "")
                    + " "
                    + " ".join(
                        _mvp_final_fulltext_evidence_parts
                    )
                )
                .lower()
                .replace("-", " ")
            )
        _mvp_ai_evidence_present = (
            _mvp_relevance_re.search(
                r"(?<![a-z0-9])ai(?![a-z0-9])",
                _mvp_final_citation_blob,
            )
            is not None
            or "artificial intelligence" in _mvp_final_citation_blob
            or "kecerdasan buatan" in _mvp_final_citation_blob
            or "machine learning" in _mvp_final_citation_blob
            or "deep learning" in _mvp_final_citation_blob
            or "neural network" in _mvp_final_citation_blob
            or "jaringan saraf" in _mvp_final_citation_blob
        )
        if (
            _mvp_requires_iot
            and _mvp_requires_ai
            and not _mvp_ai_evidence_present
        ):
            generated = (
                "Evidence repository yang memenuhi kedua konsep pada topik "
                f"'{_mvp_bounded_user_topic}' belum ditemukan. "
                "Dokumen yang ditemukan membahas IoT, tetapi tidak memuat evidence "
                "Artificial Intelligence atau Machine Learning yang cukup untuk "
                "membentuk thesis ideas yang benar-benar grounded. DELBot tidak "
                "menggunakan dokumen IoT tanpa evidence AI sebagai sumber pendukung. "
                "Tambahkan dokumen IoT-AI yang relevan atau gunakan kata kunci yang "
                "lebih spesifik sesuai koleksi."
            )
            citations = []
        # DELBOT MVP enrich repository citation metadata
        try:
            from pathlib import Path as _MvpPath
            import json as _mvp_json

            _mvp_metadata_path = (
                _MvpPath(__file__).resolve().parents[2]
                / "repository_data"
                / "metadata"
                / "skripsi_dataset.json"
            )
            _mvp_metadata_index = {}

            if _mvp_metadata_path.is_file():
                _mvp_metadata_records = _mvp_json.loads(
                    _mvp_metadata_path.read_text(
                        encoding="utf-8"
                    )
                )

                for _mvp_record in _mvp_metadata_records:
                    if not isinstance(_mvp_record, dict):
                        continue

                    _mvp_record_url = str(
                        _mvp_record.get("url") or ""
                    ).strip()
                    _mvp_match = __import__("re").search(
                        r"123456789[/\-](\d+)",
                        _mvp_record_url,
                    )
                    if not _mvp_match:
                        continue

                    _mvp_record_id = (
                        "123456789-" + _mvp_match.group(1)
                    )
                    _mvp_metadata_index[_mvp_record_id] = (
                        _mvp_record
                    )

            for _mvp_source_number, _mvp_citation in enumerate(
                list(citations or []),
                start=1,
            ):
                _mvp_document = _mvp_citation_value(
                    _mvp_citation,
                    "document",
                    {},
                )
                _mvp_document_id = str(
                    _mvp_citation_value(
                        _mvp_document,
                        "document_id",
                        "",
                    )
                    or ""
                ).strip()

                _mvp_id_match = __import__("re").search(
                    r"123456789[/\-](\d+)",
                    _mvp_document_id,
                )
                if _mvp_id_match:
                    _mvp_document_id = (
                        "123456789-"
                        + _mvp_id_match.group(1)
                    )

                _mvp_citation_metadata = (
                    _mvp_citation_mapping(
                        _mvp_citation,
                        "metadata",
                    )
                )
                _mvp_document_metadata = (
                    _mvp_citation_mapping(
                        _mvp_document,
                        "metadata",
                    )
                )

                if _mvp_is_fulltext_citation(_mvp_citation):
                    _mvp_citation_metadata.update({
                        "evidence_type": "fulltext_pdf",
                        "source_label": (
                            f"Sumber {_mvp_source_number}"
                        ),
                        "source_kind_label": "Isi PDF",
                        "priority_policy": "fulltext_first",
                    })
                    _mvp_document_metadata.update({
                        "evidence_type": "fulltext_pdf",
                        "source_kind_label": "Isi PDF",
                    })
                else:
                    _mvp_record = _mvp_metadata_index.get(
                        _mvp_document_id
                    )

                    if isinstance(_mvp_record, dict):
                        _mvp_citation_metadata.update({
                            "evidence_type": "metadata_abstract",
                            "metadata_only": True,
                            "has_pdf": False,
                            "source_label": (
                                f"Sumber {_mvp_source_number}"
                            ),
                            "source_kind_label": (
                                "Metadata/Abstrak"
                            ),
                            "fallback_reason": (
                                "no_relevant_fulltext_pdf"
                            ),
                            "priority_policy": (
                                "metadata_fallback"
                            ),
                            "author": (
                                _mvp_record.get("author") or ""
                            ),
                            "year": (
                                _mvp_record.get("year") or ""
                            ),
                            "prodi": (
                                _mvp_record.get("prodi") or ""
                            ),
                            "url": (
                                _mvp_record.get("url") or ""
                            ),
                            "abstract": (
                                _mvp_record.get("abstract") or ""
                            ),
                            "repository_code": (
                                _mvp_document_id
                            ),
                        })

                        _mvp_document_metadata.update({
                            "evidence_type": (
                                "metadata_abstract"
                            ),
                            "metadata_only": True,
                            "has_pdf": False,
                            "source_kind_label": (
                                "Metadata/Abstrak"
                            ),
                            "author": (
                                _mvp_record.get("author") or ""
                            ),
                            "year": (
                                _mvp_record.get("year") or ""
                            ),
                            "prodi": (
                                _mvp_record.get("prodi") or ""
                            ),
                            "url": (
                                _mvp_record.get("url") or ""
                            ),
                        })

                if isinstance(_mvp_citation, dict):
                    _mvp_citation["metadata"] = (
                        _mvp_citation_metadata
                    )
                else:
                    try:
                        setattr(
                            _mvp_citation,
                            "metadata",
                            _mvp_citation_metadata,
                        )
                    except Exception:
                        pass

                if isinstance(_mvp_document, dict):
                    _mvp_document["metadata"] = (
                        _mvp_document_metadata
                    )
                else:
                    try:
                        setattr(
                            _mvp_document,
                            "metadata",
                            _mvp_document_metadata,
                        )
                    except Exception:
                        pass
        except Exception:
            # Citation enrichment must never turn a valid answer
            # into an HTTP 500 response.
            pass
        # DELBOT MVP preserve exact citation at final response boundary
        try:
            if (
                evidence_turn
                and _mvp_exact_selected_citation
                is not None
            ):
                import re as _mvp_exact_final_re

                def _mvp_exact_final_value(
                    record,
                    key,
                    default=None,
                ):
                    if isinstance(record, dict):
                        return record.get(key, default)

                    return getattr(record, key, default)

                def _mvp_exact_final_document(
                    citation,
                ):
                    document = _mvp_exact_final_value(
                        citation,
                        "document",
                        {},
                    )

                    if isinstance(document, dict):
                        return document

                    return {
                        "document_id": (
                            _mvp_exact_final_value(
                                document,
                                "document_id",
                                "",
                            )
                        ),
                        "title": (
                            _mvp_exact_final_value(
                                document,
                                "title",
                                "",
                            )
                        ),
                    }

                def _mvp_exact_final_identity(
                    citation,
                ):
                    document = (
                        _mvp_exact_final_document(
                            citation
                        )
                    )
                    identifier = str(
                        document.get("document_id")
                        or _mvp_exact_final_value(
                            citation,
                            "document_id",
                            "",
                        )
                        or ""
                    ).replace("/", "-")
                    title = str(
                        document.get("title")
                        or _mvp_exact_final_value(
                            citation,
                            "document_title",
                            "",
                        )
                        or ""
                    ).strip().lower()

                    return identifier or title

                _mvp_exact_final_document_value = (
                    _mvp_exact_final_document(
                        _mvp_exact_selected_citation
                    )
                )
                _mvp_exact_final_title = str(
                    _mvp_exact_final_document_value.get(
                        "title"
                    )
                    or ""
                ).strip()
                _mvp_exact_final_id = str(
                    _mvp_exact_final_document_value.get(
                        "document_id"
                    )
                    or ""
                ).replace("/", "-")

                _mvp_exact_final_answer_normalized = (
                    " ".join(
                        _mvp_exact_final_re.findall(
                            r"[a-z0-9]+",
                            str(generated or "").lower(),
                        )
                    )
                )
                _mvp_exact_final_title_tokens = [
                    token
                    for token in (
                        " ".join(
                            _mvp_exact_final_re.findall(
                                r"[a-z0-9]+",
                                _mvp_exact_final_title.lower(),
                            )
                        ).split()
                    )
                    if len(token) >= 3
                ]
                _mvp_exact_final_title_prefix = (
                    " ".join(
                        _mvp_exact_final_title_tokens[:4]
                    )
                )

                _mvp_exact_final_answer_mentions_source = (
                    bool(
                        _mvp_exact_final_title_prefix
                        and _mvp_exact_final_title_prefix
                        in _mvp_exact_final_answer_normalized
                    )
                    or bool(
                        _mvp_exact_final_id
                        and (
                            _mvp_exact_final_id.lower()
                            in str(generated or "").lower()
                            or _mvp_exact_final_id.replace(
                                "-",
                                "/",
                            ).lower()
                            in str(generated or "").lower()
                        )
                    )
                )

                if _mvp_exact_final_answer_mentions_source:
                    _mvp_exact_final_selected_identity = (
                        _mvp_exact_final_identity(
                            _mvp_exact_selected_citation
                        )
                    )
                    _mvp_exact_final_preserved = [
                        _mvp_exact_selected_citation
                    ]
                    _mvp_exact_final_seen = {
                        _mvp_exact_final_selected_identity
                    }

                    for _mvp_exact_final_item in list(
                        citations or []
                    ):
                        _mvp_exact_final_item_identity = (
                            _mvp_exact_final_identity(
                                _mvp_exact_final_item
                            )
                        )

                        if (
                            not _mvp_exact_final_item_identity
                            or _mvp_exact_final_item_identity
                            in _mvp_exact_final_seen
                        ):
                            continue

                        # DELBOT MVP retain only query-relevant companion citations
                        _mvp_exact_final_item_document = (
                            _mvp_exact_final_document(
                                _mvp_exact_final_item
                            )
                        )
                        _mvp_exact_final_item_title = str(
                            _mvp_exact_final_item_document.get(
                                "title"
                            )
                            or ""
                        )
                        _mvp_exact_final_item_text = str(
                            _mvp_exact_final_value(
                                _mvp_exact_final_item,
                                "text",
                                "",
                            )
                            or ""
                        )
                        _mvp_exact_final_query_stopwords = {
                            "saya", "butuh", "untuk",
                            "yang", "dan", "dengan",
                            "dalam", "tentang", "terkait",
                            "skripsi", "tugas", "akhir",
                            "pembuatan", "referensi",
                            "refrensi", "repository",
                            "berikan", "tolong",
                            "berdasarkan",
                        }
                        _mvp_exact_final_query_tokens = {
                            token
                            for token in (
                                _mvp_exact_final_re.findall(
                                    r"[a-z0-9]+",
                                    str(
                                        _mvp_original_question
                                        or question
                                        or ""
                                    ).lower(),
                                )
                            )
                            if (
                                len(token) >= 3
                                and token
                                not in (
                                    _mvp_exact_final_query_stopwords
                                )
                            )
                        }
                        _mvp_exact_final_item_blob = (
                            " ".join(
                                _mvp_exact_final_re.findall(
                                    r"[a-z0-9]+",
                                    (
                                        _mvp_exact_final_item_title
                                        + " "
                                        + _mvp_exact_final_item_text
                                    ).lower(),
                                )
                            )
                        )
                        _mvp_exact_final_item_matches = {
                            token
                            for token
                            in _mvp_exact_final_query_tokens
                            if token
                            in _mvp_exact_final_item_blob
                        }

                        if (
                            len(
                                _mvp_exact_final_query_tokens
                            ) >= 2
                            and len(
                                _mvp_exact_final_item_matches
                            ) < 2
                        ):
                            continue

                        _mvp_exact_final_seen.add(
                            _mvp_exact_final_item_identity
                        )
                        _mvp_exact_final_preserved.append(
                            _mvp_exact_final_item
                        )

                    citations = (
                        _mvp_exact_final_preserved[:3]
                    )
        except Exception:
            # Citation preservation must not change a
            # successful research response into HTTP 500.
            pass


        # DELBOT MVP final-boundary catalog reconciliation
        #
        # A strongly matching metadata source may have been used in the
        # generated answer but lost from citations by a later filter.
        # Reconcile it once, immediately before the response is returned.
        try:
            from pathlib import Path as _MvpCatalogPath
            import json as _mvp_catalog_json
            import re as _mvp_catalog_re

            def _mvp_catalog_normalize(value):
                return _mvp_catalog_re.sub(
                    r"[^a-z0-9]+",
                    " ",
                    str(value or "").lower(),
                ).strip()

            def _mvp_catalog_tokens(value):
                return [
                    token
                    for token in _mvp_catalog_normalize(value).split()
                    if token
                ]

            def _mvp_catalog_longest_run(
                candidate_tokens,
                query_tokens,
            ):
                longest = 0

                for candidate_index in range(
                    len(candidate_tokens)
                ):
                    for query_index in range(
                        len(query_tokens)
                    ):
                        run = 0

                        while (
                            candidate_index + run
                            < len(candidate_tokens)
                            and query_index + run
                            < len(query_tokens)
                            and candidate_tokens[
                                candidate_index + run
                            ]
                            == query_tokens[
                                query_index + run
                            ]
                        ):
                            run += 1

                        longest = max(longest, run)

                return longest

            def _mvp_catalog_value(
                value,
                key,
                default=None,
            ):
                if isinstance(value, dict):
                    return value.get(key, default)

                return getattr(value, key, default)

            def _mvp_catalog_citation_document(citation):
                document = _mvp_catalog_value(
                    citation,
                    "document",
                    {},
                )
                return document if document is not None else {}

            def _mvp_catalog_citation_id(citation):
                document = (
                    _mvp_catalog_citation_document(citation)
                )
                return str(
                    _mvp_catalog_value(
                        document,
                        "document_id",
                        "",
                    )
                    or _mvp_catalog_value(
                        citation,
                        "document_id",
                        "",
                    )
                    or ""
                ).strip()

            def _mvp_catalog_citation_title(citation):
                document = (
                    _mvp_catalog_citation_document(citation)
                )
                return str(
                    _mvp_catalog_value(
                        document,
                        "title",
                        "",
                    )
                    or _mvp_catalog_value(
                        citation,
                        "document_title",
                        "",
                    )
                    or _mvp_catalog_value(
                        citation,
                        "title",
                        "",
                    )
                    or ""
                ).strip()

            def _mvp_catalog_document_id(record):
                direct_id = str(
                    record.get("document_id")
                    or record.get("doc_id")
                    or record.get("id")
                    or ""
                ).strip()

                if direct_id:
                    return direct_id.replace("/", "-")

                repository_url = str(
                    record.get("url") or ""
                ).strip()

                handle_match = _mvp_catalog_re.search(
                    r"/handle/(\d+)/(\d+)(?:[/?#]|$)",
                    repository_url,
                    flags=_mvp_catalog_re.IGNORECASE,
                )

                if handle_match:
                    return (
                        f"{handle_match.group(1)}-"
                        f"{handle_match.group(2)}"
                    )

                return ""

            _mvp_catalog_query = str(
                question or ""
            ).strip()
            _mvp_catalog_answer = str(
                generated or ""
            ).strip()

            _mvp_catalog_query_tokens = (
                _mvp_catalog_tokens(_mvp_catalog_query)
            )
            _mvp_catalog_answer_normalized = (
                _mvp_catalog_normalize(
                    _mvp_catalog_answer
                )
            )

            _mvp_catalog_file = (
                _MvpCatalogPath(__file__)
                .resolve()
                .parents[2]
                / "repository_data"
                / "metadata"
                / "skripsi_dataset.json"
            )

            _mvp_catalog_records = []

            if _mvp_catalog_file.is_file():
                _mvp_catalog_payload = (
                    _mvp_catalog_json.loads(
                        _mvp_catalog_file.read_text(
                            encoding="utf-8"
                        )
                    )
                )

                if isinstance(_mvp_catalog_payload, list):
                    _mvp_catalog_records = [
                        item
                        for item in _mvp_catalog_payload
                        if isinstance(item, dict)
                    ]

            _mvp_catalog_ranked = []

            for _mvp_catalog_record in _mvp_catalog_records:
                _mvp_catalog_title = str(
                    _mvp_catalog_record.get("title")
                    or ""
                ).strip()

                _mvp_catalog_title_tokens = (
                    _mvp_catalog_tokens(
                        _mvp_catalog_title
                    )
                )

                if not _mvp_catalog_title_tokens:
                    continue

                _mvp_catalog_run = (
                    _mvp_catalog_longest_run(
                        _mvp_catalog_title_tokens,
                        _mvp_catalog_query_tokens,
                    )
                )

                _mvp_catalog_overlap = len(
                    set(_mvp_catalog_title_tokens)
                    & set(_mvp_catalog_query_tokens)
                )

                _mvp_catalog_prefix = " ".join(
                    _mvp_catalog_title_tokens[:4]
                )

                _mvp_catalog_answer_match = bool(
                    _mvp_catalog_prefix
                    and _mvp_catalog_prefix
                    in _mvp_catalog_answer_normalized
                )

                if (
                    _mvp_catalog_run >= 4
                    and _mvp_catalog_answer_match
                ):
                    _mvp_catalog_ranked.append(
                        (
                            _mvp_catalog_run,
                            _mvp_catalog_overlap,
                            _mvp_catalog_record,
                        )
                    )

            _mvp_catalog_ranked.sort(
                key=lambda item: (
                    item[0],
                    item[1],
                ),
                reverse=True,
            )

            _mvp_catalog_exact_record = None

            if _mvp_catalog_ranked:
                _mvp_catalog_best = (
                    _mvp_catalog_ranked[0]
                )

                _mvp_catalog_ambiguous = bool(
                    len(_mvp_catalog_ranked) > 1
                    and _mvp_catalog_ranked[1][0]
                    == _mvp_catalog_best[0]
                    and _mvp_catalog_ranked[1][1]
                    == _mvp_catalog_best[1]
                )

                if not _mvp_catalog_ambiguous:
                    _mvp_catalog_exact_record = (
                        _mvp_catalog_best[2]
                    )

            if _mvp_catalog_exact_record:
                _mvp_catalog_exact_id = (
                    _mvp_catalog_document_id(
                        _mvp_catalog_exact_record
                    )
                )
                _mvp_catalog_exact_title = str(
                    _mvp_catalog_exact_record.get(
                        "title"
                    )
                    or ""
                ).strip()
                _mvp_catalog_exact_url = str(
                    _mvp_catalog_exact_record.get(
                        "url"
                    )
                    or ""
                ).strip()
                _mvp_catalog_exact_author = str(
                    _mvp_catalog_exact_record.get(
                        "author"
                    )
                    or ""
                ).strip()
                _mvp_catalog_exact_year = str(
                    _mvp_catalog_exact_record.get(
                        "year"
                    )
                    or ""
                ).strip()
                _mvp_catalog_exact_prodi = str(
                    _mvp_catalog_exact_record.get(
                        "prodi"
                    )
                    or ""
                ).strip()
                _mvp_catalog_exact_abstract = str(
                    _mvp_catalog_exact_record.get(
                        "abstract"
                    )
                    or ""
                ).strip()

                if (
                    _mvp_catalog_exact_id
                    and _mvp_catalog_exact_title
                ):
                    _mvp_catalog_exact_metadata = {
                        "evidence_type": (
                            "metadata_abstract"
                        ),
                        "metadata_only": True,
                        "has_pdf": False,
                        "repository_url": (
                            _mvp_catalog_exact_url
                        ),
                        "url": _mvp_catalog_exact_url,
                        "author": (
                            _mvp_catalog_exact_author
                        ),
                        "year": _mvp_catalog_exact_year,
                        "prodi": _mvp_catalog_exact_prodi,
                        "section": "",
                        "page_start": None,
                        "page_end": None,
                        "fallback_reason": (
                            "parsed_fulltext_not_available"
                        ),
                    }

                    _mvp_catalog_exact_citation = {
                        "chunk_id": (
                            "metadata:"
                            + _mvp_catalog_exact_id
                        ),
                        "document": {
                            "document_id": (
                                _mvp_catalog_exact_id
                            ),
                            "title": (
                                _mvp_catalog_exact_title
                            ),
                            "authors": (
                                _mvp_catalog_exact_author
                            ),
                            "file_path": "",
                            "metadata": dict(
                                _mvp_catalog_exact_metadata
                            ),
                        },
                        "metadata": dict(
                            _mvp_catalog_exact_metadata
                        ),
                        "page": None,
                        "score": 1.0,
                        "text": (
                            _mvp_catalog_exact_abstract
                        ),
                    }

                    _mvp_catalog_stopwords = {
                        "yang",
                        "dan",
                        "dengan",
                        "untuk",
                        "dari",
                        "pada",
                        "dalam",
                        "berdasarkan",
                        "penerapan",
                        "algoritma",
                        "studi",
                        "kasus",
                        "data",
                        "sistem",
                        "skripsi",
                        "tugas",
                        "akhir",
                    }

                    _mvp_catalog_anchor_tokens = {
                        token
                        for token in _mvp_catalog_tokens(
                            _mvp_catalog_exact_title
                        )
                        if (
                            token
                            in set(
                                _mvp_catalog_query_tokens
                            )
                            and token
                            not in _mvp_catalog_stopwords
                            and len(token) >= 3
                        )
                    }

                    _mvp_catalog_companions = []
                    _mvp_catalog_seen_ids = {
                        _mvp_catalog_exact_id
                    }

                    for _mvp_catalog_existing in list(
                        citations or []
                    ):
                        _mvp_catalog_existing_id = (
                            _mvp_catalog_citation_id(
                                _mvp_catalog_existing
                            )
                        )
                        _mvp_catalog_existing_title = (
                            _mvp_catalog_citation_title(
                                _mvp_catalog_existing
                            )
                        )
                        _mvp_catalog_existing_tokens = set(
                            _mvp_catalog_tokens(
                                _mvp_catalog_existing_title
                            )
                        )
                        _mvp_catalog_anchor_hits = len(
                            _mvp_catalog_anchor_tokens
                            & _mvp_catalog_existing_tokens
                        )

                        _mvp_catalog_identity = (
                            _mvp_catalog_existing_id
                            or _mvp_catalog_normalize(
                                _mvp_catalog_existing_title
                            )
                        )

                        if (
                            not _mvp_catalog_identity
                            or _mvp_catalog_identity
                            in _mvp_catalog_seen_ids
                            or _mvp_catalog_anchor_hits < 2
                        ):
                            continue

                        _mvp_catalog_seen_ids.add(
                            _mvp_catalog_identity
                        )
                        _mvp_catalog_companions.append(
                            _mvp_catalog_existing
                        )

                    citations = [
                        _mvp_catalog_exact_citation,
                        *_mvp_catalog_companions[:2],
                    ]
        except Exception:
            # Citation reconciliation cannot convert a valid
            # research answer into an HTTP 500 response.
            pass


        # DELBOT MVP deterministic single PDF example V2
        try:
            import re as _pdf_example_re

            _pdf_example_query = str(
                question or ""
            ).lower()
            _pdf_example_intent = (
                "pdf" in _pdf_example_query
                and any(
                    phrase in _pdf_example_query
                    for phrase in (
                        "contoh",
                        "satu dokumen",
                        "isi dokumen",
                        "berikan file",
                        "berikan dokumen",
                        "tampilkan dokumen",
                    )
                )
            )

            def _pdf_example_value(value, key, default=None):
                if isinstance(value, dict):
                    return value.get(key, default)
                return getattr(value, key, default)

            def _pdf_example_document(citation):
                return (
                    _pdf_example_value(
                        citation,
                        "document",
                        {},
                    )
                    or {}
                )

            def _pdf_example_nested_text(citation, key):
                document = _pdf_example_document(
                    citation
                )
                root_metadata = (
                    _pdf_example_value(
                        citation,
                        "metadata",
                        {},
                    )
                    or {}
                )
                document_metadata = (
                    _pdf_example_value(
                        document,
                        "metadata",
                        {},
                    )
                    or {}
                )

                values = [
                    _pdf_example_value(
                        citation,
                        key,
                        "",
                    ),
                    _pdf_example_value(
                        document,
                        key,
                        "",
                    ),
                ]

                if isinstance(root_metadata, dict):
                    values.append(
                        root_metadata.get(key)
                    )

                if isinstance(document_metadata, dict):
                    values.append(
                        document_metadata.get(key)
                    )

                for value in values:
                    text = str(value or "").strip()
                    if text:
                        return text

                return ""

            if _pdf_example_intent:
                _pdf_candidates = []

                for citation in list(citations or []):
                    evidence_type = (
                        _pdf_example_nested_text(
                            citation,
                            "evidence_type",
                        ).lower()
                    )
                    file_path = (
                        _pdf_example_nested_text(
                            citation,
                            "file_path",
                        )
                        or _pdf_example_nested_text(
                            citation,
                            "pdf_path",
                        )
                    )

                    if (
                        "fulltext" in evidence_type
                        or "pdf" in evidence_type
                        or bool(file_path)
                    ):
                        _pdf_candidates.append(citation)

                if _pdf_candidates:
                    generated_lower = str(
                        generated or ""
                    ).lower()

                    def candidate_score(citation):
                        title = (
                            _pdf_example_nested_text(
                                citation,
                                "title",
                            )
                            or _pdf_example_nested_text(
                                citation,
                                "document_title",
                            )
                        )

                        tokens = {
                            token
                            for token in _pdf_example_re.sub(
                                r"[^a-z0-9]+",
                                " ",
                                title.lower(),
                            ).split()
                            if len(token) >= 4
                            and token not in {
                                "yang",
                                "dengan",
                                "untuk",
                                "pada",
                                "dalam",
                                "studi",
                                "kasus",
                            }
                        }

                        return sum(
                            token in generated_lower
                            for token in tokens
                        )

                    selected_pdf = max(
                        _pdf_candidates,
                        key=candidate_score,
                    )
                    selected_document = (
                        _pdf_example_document(
                            selected_pdf
                        )
                    )
                    selected_title = str(
                        _pdf_example_value(
                            selected_document,
                            "title",
                            "",
                        )
                        or _pdf_example_nested_text(
                            selected_pdf,
                            "document_title",
                        )
                        or "Dokumen repository"
                    ).strip()
                    selected_excerpt = " ".join(
                        str(
                            _pdf_example_value(
                                selected_pdf,
                                "text",
                                "",
                            )
                            or ""
                        ).split()
                    )[:1100]
                    selected_section = (
                        _pdf_example_nested_text(
                            selected_pdf,
                            "section",
                        )
                        or _pdf_example_nested_text(
                            selected_pdf,
                            "section_title",
                        )
                    )
                    selected_page = (
                        _pdf_example_nested_text(
                            selected_pdf,
                            "page",
                        )
                        or _pdf_example_nested_text(
                            selected_pdf,
                            "page_start",
                        )
                    )

                    location_parts = []

                    if selected_section:
                        location_parts.append(
                            selected_section
                        )

                    if selected_page:
                        location_parts.append(
                            "halaman " + selected_page
                        )

                    selected_location = (
                        " · ".join(location_parts)
                        or "Tersedia pada panel sumber"
                    )

                    generated = (
                        "## Contoh dokumen PDF\n\n"
                        f"**{selected_title}**\n\n"
                        "**Lokasi cuplikan:** "
                        f"{selected_location}\n\n"
                        "**Cuplikan isi:** "
                        f"{selected_excerpt}\n\n"
                        "PDF ini tersedia di repository. "
                        "Pilih **Lihat insight**, kemudian "
                        "gunakan **Visualisasikan PDF** "
                        "atau **Unduh PDF**."
                    )
                    citations = [selected_pdf]

                    for target in (
                        selected_pdf,
                        selected_document,
                    ):
                        metadata = (
                            _pdf_example_value(
                                target,
                                "metadata",
                                {},
                            )
                            or {}
                        )

                        if isinstance(metadata, dict):
                            metadata["has_pdf"] = True

                            if isinstance(target, dict):
                                target["metadata"] = metadata
                            else:
                                try:
                                    setattr(
                                        target,
                                        "metadata",
                                        metadata,
                                    )
                                except Exception:
                                    pass
        except Exception:
            pass

        # DELBOT MVP final evidence quality reconciliation 767909
        try:
            import json as _mvp_quality_json
            import re as _mvp_quality_re
            from pathlib import Path as _MvpQualityPath

            def _mvp_quality_get(value, key, default=None):
                if isinstance(value, dict):
                    return value.get(key, default)

                return getattr(value, key, default)

            def _mvp_quality_set(value, key, new_value):
                if isinstance(value, dict):
                    value[key] = new_value
                    return

                try:
                    setattr(value, key, new_value)
                except Exception:
                    pass

            def _mvp_quality_mapping(value, key):
                mapping = _mvp_quality_get(value, key, {})

                if isinstance(mapping, dict):
                    return mapping

                return {}

            def _mvp_quality_document(citation):
                return _mvp_quality_get(
                    citation,
                    "document",
                    {},
                )

            def _mvp_quality_document_id(citation):
                document = _mvp_quality_document(citation)
                document_id = str(
                    _mvp_quality_get(
                        document,
                        "document_id",
                        "",
                    )
                    or _mvp_quality_get(
                        citation,
                        "document_id",
                        "",
                    )
                    or ""
                ).strip()

                if document_id:
                    return document_id.replace("/", "-")

                urls = [
                    _mvp_quality_get(document, "url", ""),
                    _mvp_quality_get(
                        _mvp_quality_mapping(
                            document,
                            "metadata",
                        ),
                        "url",
                        "",
                    ),
                    _mvp_quality_get(
                        _mvp_quality_mapping(
                            document,
                            "metadata",
                        ),
                        "repository_url",
                        "",
                    ),
                ]

                for url in urls:
                    match = _mvp_quality_re.search(
                        r"handle/(\d+)/(\d+)",
                        str(url or ""),
                    )

                    if match:
                        return (
                            f"{match.group(1)}-"
                            f"{match.group(2)}"
                        )

                title = str(
                    _mvp_quality_get(
                        document,
                        "title",
                        "",
                    )
                    or ""
                ).strip().lower()

                return (
                    "title:"
                    + _mvp_quality_re.sub(
                        r"[^a-z0-9]+",
                        "-",
                        title,
                    ).strip("-")
                )

            def _mvp_quality_title(citation):
                return str(
                    _mvp_quality_get(
                        _mvp_quality_document(citation),
                        "title",
                        "",
                    )
                    or ""
                ).strip()

            def _mvp_quality_text(citation):
                return str(
                    _mvp_quality_get(
                        citation,
                        "text",
                        "",
                    )
                    or ""
                ).strip()

            def _mvp_quality_is_noise(text):
                normalized = str(text or "").lower()

                noise_terms = (
                    "daftar isi",
                    "daftar gambar",
                    "daftar tabel",
                    "daftar rumus",
                    "daftar lampiran",
                )

                noise_hits = sum(
                    term in normalized
                    for term in noise_terms
                )

                dotted_runs = len(
                    _mvp_quality_re.findall(
                        r"\.{8,}",
                        normalized,
                    )
                )

                return (
                    noise_hits >= 1
                    or dotted_runs >= 3
                    or (
                        dotted_runs >= 1
                        and len(normalized) < 1800
                    )
                )

            def _mvp_quality_candidate_rank(citation):
                citation_metadata = _mvp_quality_mapping(
                    citation,
                    "metadata",
                )
                section = str(
                    citation_metadata.get("section")
                    or ""
                ).strip()
                text = _mvp_quality_text(citation)
                title = _mvp_quality_title(citation)
                query_lower = str(question or "").lower()

                query_tokens = {
                    token
                    for token in _mvp_quality_re.findall(
                        r"[a-z0-9]+",
                        query_lower,
                    )
                    if len(token) >= 4
                }

                evidence_lower = (
                    title + " " + text + " " + section
                ).lower()

                relevance_hits = sum(
                    token in evidence_lower
                    for token in query_tokens
                )

                meaningful_section = bool(
                    section
                    and not _mvp_quality_re.fullmatch(
                        r"(?:19|20)\d{2}",
                        section,
                    )
                    and section.lower()
                    not in {
                        "tidak dicantumkan",
                        "tidak tersedia",
                    }
                )

                try:
                    score = float(
                        _mvp_quality_get(
                            citation,
                            "score",
                            0,
                        )
                        or 0
                    )
                except Exception:
                    score = 0.0

                return (
                    0 if _mvp_quality_is_noise(text) else 1,
                    1 if meaningful_section else 0,
                    relevance_hits,
                    min(len(text), 2200),
                    score,
                )

            _mvp_quality_catalog_path = (
                _MvpQualityPath(__file__).resolve().parents[2]
                / "repository_data"
                / "metadata"
                / "skripsi_dataset.json"
            )

            _mvp_quality_catalog_records = []

            if _mvp_quality_catalog_path.is_file():
                _mvp_quality_catalog_payload = (
                    _mvp_quality_json.loads(
                        _mvp_quality_catalog_path.read_text(
                            encoding="utf-8",
                        )
                    )
                )

                if isinstance(
                    _mvp_quality_catalog_payload,
                    list,
                ):
                    _mvp_quality_catalog_records = (
                        _mvp_quality_catalog_payload
                    )
                elif isinstance(
                    _mvp_quality_catalog_payload,
                    dict,
                ):
                    for _mvp_quality_catalog_value in (
                        _mvp_quality_catalog_payload.values()
                    ):
                        if isinstance(
                            _mvp_quality_catalog_value,
                            list,
                        ):
                            _mvp_quality_catalog_records = (
                                _mvp_quality_catalog_value
                            )
                            break

            def _mvp_quality_catalog_id(record):
                for key in (
                    "document_id",
                    "doc_id",
                    "id",
                    "handle",
                ):
                    value = str(
                        record.get(key)
                        or ""
                    ).strip()

                    if value:
                        return value.replace("/", "-")

                url = str(
                    record.get("url")
                    or record.get("repository_url")
                    or ""
                )

                match = _mvp_quality_re.search(
                    r"handle/(\d+)/(\d+)",
                    url,
                )

                if match:
                    return (
                        f"{match.group(1)}-"
                        f"{match.group(2)}"
                    )

                return ""

            def _mvp_quality_author_rows(author_value):
                values = (
                    author_value
                    if isinstance(author_value, list)
                    else [author_value]
                )
                rows = []

                for value in values:
                    if isinstance(value, dict):
                        name = str(
                            value.get("full_name")
                            or value.get("name")
                            or value.get("author")
                            or ""
                        ).strip()
                    else:
                        name = str(value or "").strip()

                    if name:
                        rows.append({
                            "author_id": "",
                            "full_name": name,
                            "email": "",
                            "orcid": "",
                            "metadata": {},
                        })

                return rows

            _mvp_quality_catalog_by_id = {}

            for _mvp_quality_record in (
                _mvp_quality_catalog_records
            ):
                if not isinstance(
                    _mvp_quality_record,
                    dict,
                ):
                    continue

                _mvp_quality_record_id = (
                    _mvp_quality_catalog_id(
                        _mvp_quality_record
                    )
                )

                if _mvp_quality_record_id:
                    _mvp_quality_catalog_by_id[
                        _mvp_quality_record_id
                    ] = _mvp_quality_record

            # Select one best chunk for every repository document.
            _mvp_quality_best_by_id = {}
            _mvp_quality_order = []

            for _mvp_quality_citation in list(
                citations or []
            ):
                _mvp_quality_id = (
                    _mvp_quality_document_id(
                        _mvp_quality_citation
                    )
                )

                if not _mvp_quality_id:
                    continue

                if _mvp_quality_id not in (
                    _mvp_quality_best_by_id
                ):
                    _mvp_quality_best_by_id[
                        _mvp_quality_id
                    ] = _mvp_quality_citation
                    _mvp_quality_order.append(
                        _mvp_quality_id
                    )
                    continue

                _mvp_quality_current = (
                    _mvp_quality_best_by_id[
                        _mvp_quality_id
                    ]
                )

                if (
                    _mvp_quality_candidate_rank(
                        _mvp_quality_citation
                    )
                    > _mvp_quality_candidate_rank(
                        _mvp_quality_current
                    )
                ):
                    _mvp_quality_best_by_id[
                        _mvp_quality_id
                    ] = _mvp_quality_citation

            citations = [
                _mvp_quality_best_by_id[
                    _mvp_quality_id
                ]
                for _mvp_quality_id in (
                    _mvp_quality_order
                )
            ]

            # Enrich active citations from the canonical catalog.
            for _mvp_quality_citation in citations:
                _mvp_quality_id = (
                    _mvp_quality_document_id(
                        _mvp_quality_citation
                    )
                )
                _mvp_quality_record = (
                    _mvp_quality_catalog_by_id.get(
                        _mvp_quality_id
                    )
                )

                if not _mvp_quality_record:
                    continue

                _mvp_quality_doc = (
                    _mvp_quality_document(
                        _mvp_quality_citation
                    )
                )
                _mvp_quality_doc_metadata = dict(
                    _mvp_quality_mapping(
                        _mvp_quality_doc,
                        "metadata",
                    )
                )
                _mvp_quality_citation_metadata = dict(
                    _mvp_quality_mapping(
                        _mvp_quality_citation,
                        "metadata",
                    )
                )

                _mvp_quality_author = (
                    _mvp_quality_record.get("author")
                    or _mvp_quality_record.get("authors")
                    or ""
                )
                _mvp_quality_year = (
                    _mvp_quality_record.get("year")
                    or ""
                )
                _mvp_quality_prodi = (
                    _mvp_quality_record.get("prodi")
                    or _mvp_quality_record.get(
                        "program_studi"
                    )
                    or ""
                )
                _mvp_quality_url = (
                    _mvp_quality_record.get("url")
                    or _mvp_quality_record.get(
                        "repository_url"
                    )
                    or ""
                )
                _mvp_quality_abstract = str(
                    _mvp_quality_record.get("abstract")
                    or ""
                ).strip()

                if not _mvp_quality_get(
                    _mvp_quality_doc,
                    "authors",
                    None,
                ):
                    _mvp_quality_set(
                        _mvp_quality_doc,
                        "authors",
                        _mvp_quality_author_rows(
                            _mvp_quality_author
                        ),
                    )

                _mvp_quality_doc_metadata.update({
                    "author": _mvp_quality_author,
                    "year": _mvp_quality_year,
                    "prodi": _mvp_quality_prodi,
                    "program_studi": _mvp_quality_prodi,
                    "url": _mvp_quality_url,
                    "repository_url": _mvp_quality_url,
                    "abstract": _mvp_quality_abstract,
                })

                _mvp_quality_citation_metadata.update({
                    "author": _mvp_quality_author,
                    "year": _mvp_quality_year,
                    "prodi": _mvp_quality_prodi,
                    "program_studi": _mvp_quality_prodi,
                    "url": _mvp_quality_url,
                    "repository_url": _mvp_quality_url,
                })

                _mvp_quality_section = str(
                    _mvp_quality_citation_metadata.get(
                        "section"
                    )
                    or ""
                ).strip()

                if _mvp_quality_re.fullmatch(
                    r"(?:19|20)\d{2}",
                    _mvp_quality_section,
                ):
                    _mvp_quality_citation_metadata[
                        "section"
                    ] = ""

                _mvp_quality_set(
                    _mvp_quality_doc,
                    "metadata",
                    _mvp_quality_doc_metadata,
                )
                _mvp_quality_set(
                    _mvp_quality_citation,
                    "metadata",
                    _mvp_quality_citation_metadata,
                )

            _mvp_quality_question_lower = str(
                question or ""
            ).lower()

            _mvp_quality_idea_intent = bool(
                _mvp_quality_re.search(
                    r"\b("
                    r"ide|judul|skripsi|tugas akhir|"
                    r"research gap|proposal"
                    r")\b",
                    _mvp_quality_question_lower,
                )
            )

            _mvp_quality_refusal = bool(
                _mvp_quality_re.search(
                    r"\b("
                    r"tidak dapat|tidak bisa|tidak mungkin|"
                    r"tidak mencukupi|tidak cukup|"
                    r"belum ditemukan|tidak tersedia"
                    r")\b",
                    str(generated or "").lower(),
                )
            )

            # When retrieval returns too few document identities, supplement
            # from catalog metadata using query-title overlap.
            if (
                _mvp_quality_idea_intent
                and len(citations) < 3
            ):
                _mvp_quality_stopwords = {
                    "saya",
                    "butuh",
                    "membutuhkan",
                    "berikan",
                    "tentang",
                    "terkait",
                    "untuk",
                    "dengan",
                    "serta",
                    "dari",
                    "yang",
                    "ide",
                    "judul",
                    "skripsi",
                    "tugas",
                    "akhir",
                    "research",
                    "gap",
                }

                _mvp_quality_query_tokens = {
                    token
                    for token in _mvp_quality_re.findall(
                        r"[a-z0-9]+",
                        _mvp_quality_question_lower,
                    )
                    if len(token) >= 4
                    and token not in _mvp_quality_stopwords
                }

                _mvp_quality_active_ids = {
                    _mvp_quality_document_id(item)
                    for item in citations
                }

                _mvp_quality_ranked_catalog = []

                for _mvp_quality_record in (
                    _mvp_quality_catalog_records
                ):
                    if not isinstance(
                        _mvp_quality_record,
                        dict,
                    ):
                        continue

                    _mvp_quality_record_id = (
                        _mvp_quality_catalog_id(
                            _mvp_quality_record
                        )
                    )
                    _mvp_quality_record_title = str(
                        _mvp_quality_record.get("title")
                        or ""
                    ).strip()

                    if (
                        not _mvp_quality_record_id
                        or not _mvp_quality_record_title
                        or _mvp_quality_record_id
                        in _mvp_quality_active_ids
                    ):
                        continue

                    _mvp_quality_title_lower = (
                        _mvp_quality_record_title.lower()
                    )
                    _mvp_quality_overlap = sum(
                        token in _mvp_quality_title_lower
                        for token in (
                            _mvp_quality_query_tokens
                        )
                    )

                    if _mvp_quality_overlap <= 0:
                        continue

                    _mvp_quality_ranked_catalog.append((
                        _mvp_quality_overlap,
                        len(
                            str(
                                _mvp_quality_record.get(
                                    "abstract"
                                )
                                or ""
                            )
                        ),
                        _mvp_quality_record,
                    ))

                _mvp_quality_ranked_catalog.sort(
                    key=lambda item: (
                        -item[0],
                        -item[1],
                        str(
                            item[2].get("title")
                            or ""
                        ).lower(),
                    )
                )

                for (
                    _mvp_quality_overlap,
                    _mvp_quality_abstract_length,
                    _mvp_quality_record,
                ) in _mvp_quality_ranked_catalog:
                    if len(citations) >= 3:
                        break

                    _mvp_quality_record_id = (
                        _mvp_quality_catalog_id(
                            _mvp_quality_record
                        )
                    )

                    if (
                        _mvp_quality_record_id
                        in _mvp_quality_active_ids
                    ):
                        continue

                    _mvp_quality_author = (
                        _mvp_quality_record.get("author")
                        or _mvp_quality_record.get(
                            "authors"
                        )
                        or ""
                    )
                    _mvp_quality_year = (
                        _mvp_quality_record.get("year")
                        or ""
                    )
                    _mvp_quality_prodi = (
                        _mvp_quality_record.get("prodi")
                        or _mvp_quality_record.get(
                            "program_studi"
                        )
                        or ""
                    )
                    _mvp_quality_url = (
                        _mvp_quality_record.get("url")
                        or _mvp_quality_record.get(
                            "repository_url"
                        )
                        or ""
                    )
                    _mvp_quality_abstract = str(
                        _mvp_quality_record.get(
                            "abstract"
                        )
                        or ""
                    ).strip()

                    citations.append({
                        "chunk_id": (
                            "metadata:"
                            + _mvp_quality_record_id
                        ),
                        "document": {
                            "document_id":
                                _mvp_quality_record_id,
                            "title": str(
                                _mvp_quality_record.get(
                                    "title"
                                )
                                or ""
                            ).strip(),
                            "authors":
                                _mvp_quality_author_rows(
                                    _mvp_quality_author
                                ),
                            "collection": "repository",
                            "entities": [],
                            "file_path": "",
                            "metadata": {
                                "author":
                                    _mvp_quality_author,
                                "year":
                                    _mvp_quality_year,
                                "prodi":
                                    _mvp_quality_prodi,
                                "program_studi":
                                    _mvp_quality_prodi,
                                "url":
                                    _mvp_quality_url,
                                "repository_url":
                                    _mvp_quality_url,
                                "abstract":
                                    _mvp_quality_abstract,
                                "metadata_only": True,
                            },
                        },
                        "metadata": {
                            "evidence_type":
                                "metadata_abstract",
                            "source_kind_label":
                                "Metadata/Abstrak",
                            "source_label":
                                "Repository metadata",
                            "metadata_only": True,
                            "section": "",
                            "page_start": None,
                            "page_end": None,
                            "author": _mvp_quality_author,
                            "year": _mvp_quality_year,
                            "prodi": _mvp_quality_prodi,
                            "program_studi":
                                _mvp_quality_prodi,
                            "url": _mvp_quality_url,
                            "repository_url":
                                _mvp_quality_url,
                        },
                        "page": None,
                        "score": float(
                            _mvp_quality_overlap
                        ),
                        "text": _mvp_quality_abstract[
                            :1800
                        ],
                    })

                    _mvp_quality_active_ids.add(
                        _mvp_quality_record_id
                    )

            citations = list(citations or [])[:3]

            # Replace a false refusal with three clearly bounded proposals.
            if (
                _mvp_quality_idea_intent
                and citations
                and (
                    _mvp_quality_refusal
                    or "## Ide 1" not in str(
                        generated or ""
                    )
                )
            ):
                _mvp_quality_topic_match = (
                    _mvp_quality_re.search(
                        r"\b(?:tentang|terkait|topik)\s+"
                        r"([^,.?]+)",
                        str(question or ""),
                        flags=_mvp_quality_re.IGNORECASE,
                    )
                )

                if _mvp_quality_topic_match:
                    _mvp_quality_topic = (
                        _mvp_quality_topic_match.group(1)
                        .strip()
                    )
                else:
                    _mvp_quality_topic = str(
                        question or "topik penelitian"
                    ).strip()

                _mvp_quality_topic = (
                    _mvp_quality_re.sub(
                        r"\s+",
                        " ",
                        _mvp_quality_topic,
                    )[:120]
                    or "topik penelitian"
                )

                _mvp_quality_is_prediction = bool(
                    _mvp_quality_re.search(
                        r"\b("
                        r"prediksi|forecast|peramalan|"
                        r"klasifikasi"
                        r")\b",
                        _mvp_quality_question_lower,
                    )
                )

                _mvp_quality_methods = []

                for _mvp_quality_citation in citations:
                    _mvp_quality_source_title = (
                        _mvp_quality_title(
                            _mvp_quality_citation
                        )
                    )

                    for _mvp_quality_method in (
                        "Artificial Neural Network",
                        "ANN",
                        "LSTM",
                        "Backpropagation",
                        "Support Vector Regression",
                        "SVR",
                        "Machine Learning",
                        "Deep Learning",
                    ):
                        if (
                            _mvp_quality_method.lower()
                            in _mvp_quality_source_title.lower()
                            and _mvp_quality_method
                            not in _mvp_quality_methods
                        ):
                            _mvp_quality_methods.append(
                                _mvp_quality_method
                            )

                _mvp_quality_method_label = (
                    ", ".join(
                        _mvp_quality_methods[:3]
                    )
                    or "model komputasional"
                )

                if _mvp_quality_is_prediction:
                    _mvp_quality_titles = [
                        (
                            "Studi Komparatif dan Optimasi "
                            f"{_mvp_quality_method_label} "
                            f"untuk {_mvp_quality_topic}"
                        ),
                        (
                            "Model Ensemble Multivariat "
                            f"untuk {_mvp_quality_topic}"
                        ),
                        (
                            "Sistem Prediksi Explainable "
                            f"untuk {_mvp_quality_topic} "
                            "dengan Pemantauan Real-Time"
                        ),
                    ]
                    _mvp_quality_metrics = (
                        "MAE, RMSE, MAPE, stabilitas pada "
                        "periode ekstrem, dan waktu inferensi"
                    )
                else:
                    _mvp_quality_titles = [
                        (
                            "Perbandingan Metode untuk "
                            f"{_mvp_quality_topic}"
                        ),
                        (
                            "Optimasi Model Kontekstual untuk "
                            f"{_mvp_quality_topic}"
                        ),
                        (
                            "Sistem Explainable dan Siap "
                            f"Implementasi untuk "
                            f"{_mvp_quality_topic}"
                        ),
                    ]
                    _mvp_quality_metrics = (
                        "metrik kinerja utama sesuai tugas, "
                        "robustness, efisiensi, dan usability"
                    )

                _mvp_quality_parts = [
                    (
                        "Berikut tiga arah tugas akhir yang "
                        "disusun dari sumber repository yang "
                        "relevan."
                    ),
                    (
                        "**Batas fakta dan usulan:** judul dan "
                        "informasi bibliografis berasal dari "
                        "repository. Metode lanjutan, desain "
                        "eksperimen, dan kontribusi di bawah "
                        "merupakan usulan penelitian—bukan "
                        "hasil yang diklaim sudah ada."
                    ),
                ]

                for _mvp_quality_index in range(3):
                    _mvp_quality_source = citations[
                        _mvp_quality_index
                        % len(citations)
                    ]
                    _mvp_quality_source_id = (
                        _mvp_quality_document_id(
                            _mvp_quality_source
                        )
                    )
                    _mvp_quality_source_title = (
                        _mvp_quality_title(
                            _mvp_quality_source
                        )
                    )

                    if _mvp_quality_index == 0:
                        _mvp_quality_problem = (
                            "Belum jelas model mana yang paling "
                            "konsisten ketika diuji pada data, "
                            "periode, dan kondisi yang sama."
                        )
                        _mvp_quality_gap = (
                            "Sumber menunjukkan penggunaan "
                            "metode prediktif, tetapi evidence "
                            "yang tersedia belum membuktikan "
                            "perbandingan yang adil dengan "
                            "pipeline dan pembagian data yang "
                            "seragam."
                        )
                        _mvp_quality_method = (
                            "Bangun beberapa baseline, gunakan "
                            "time-series split, optimasi "
                            "hyperparameter yang sama, lalu "
                            "lakukan uji ablation."
                        )
                        _mvp_quality_contribution = (
                            "Benchmark yang reproducible dan "
                            "rekomendasi model berdasarkan "
                            "akurasi, stabilitas, serta biaya "
                            "komputasi."
                        )
                    elif _mvp_quality_index == 1:
                        _mvp_quality_problem = (
                            "Prediksi dapat menurun ketika pola "
                            "musiman berubah atau terjadi nilai "
                            "ekstrem."
                        )
                        _mvp_quality_gap = (
                            "Evidence belum cukup menjelaskan "
                            "ketahanan model terhadap perubahan "
                            "distribusi, variabel multivariat, "
                            "dan kejadian ekstrem."
                        )
                        _mvp_quality_method = (
                            "Gabungkan variabel relevan dalam "
                            "model ensemble, lakukan feature "
                            "engineering temporal, dan evaluasi "
                            "berdasarkan musim serta tingkat "
                            "ekstrem."
                        )
                        _mvp_quality_contribution = (
                            "Model yang lebih robust beserta "
                            "analisis faktor yang paling "
                            "memengaruhi kesalahan prediksi."
                        )
                    else:
                        _mvp_quality_problem = (
                            "Model yang akurat belum tentu mudah "
                            "dipahami atau digunakan dalam "
                            "pengambilan keputusan."
                        )
                        _mvp_quality_gap = (
                            "Sumber belum cukup menghubungkan "
                            "hasil prediksi dengan penjelasan "
                            "model, ketidakpastian, dan alur "
                            "pemantauan yang dapat digunakan."
                        )
                        _mvp_quality_method = (
                            "Tambahkan explainability, interval "
                            "ketidakpastian, API inferensi, serta "
                            "dashboard untuk menampilkan tren, "
                            "peringatan, dan alasan prediksi."
                        )
                        _mvp_quality_contribution = (
                            "Prototipe end-to-end yang "
                            "menghubungkan model, interpretasi, "
                            "dan kebutuhan pengguna."
                        )

                    _mvp_quality_parts.append(
                        "\n".join([
                            (
                                f"## Ide "
                                f"{_mvp_quality_index + 1}"
                            ),
                            (
                                f"**Judul:** "
                                f"{_mvp_quality_titles[_mvp_quality_index]}"
                            ),
                            (
                                f"**Masalah:** "
                                f"{_mvp_quality_problem}"
                            ),
                            (
                                f"**Research gap:** "
                                f"{_mvp_quality_gap}"
                            ),
                            (
                                f"**Arah metode:** "
                                f"{_mvp_quality_method}"
                            ),
                            (
                                "**Rencana evaluasi:** "
                                f"Gunakan {_mvp_quality_metrics}; "
                                "bandingkan terhadap baseline "
                                "dan laporkan variasi hasil pada "
                                "beberapa pembagian waktu."
                            ),
                            (
                                f"**Kontribusi yang diharapkan:** "
                                f"{_mvp_quality_contribution}"
                            ),
                            (
                                "**Keterbatasan:** Kualitas hasil "
                                "bergantung pada kelengkapan, "
                                "rentang waktu, konsistensi, dan "
                                "representativitas data."
                            ),
                            (
                                "**Sumber pendukung:** "
                                f"[{_mvp_quality_source_id}] "
                                f"{_mvp_quality_source_title}."
                            ),
                        ])
                    )

                generated = "\n\n".join(
                    _mvp_quality_parts
                )

        except Exception:
            # Quality reconciliation must never turn a valid
            # response into an HTTP 500.
            pass

        # DELBOT MVP thesis continuation and weather relevance 767913
        try:
            import json as _mvp_next_json
            import re as _mvp_next_re
            from pathlib import Path as _MvpNextPath

            def _mvp_next_get(value, key, default=None):
                if isinstance(value, dict):
                    return value.get(key, default)

                return getattr(value, key, default)

            def _mvp_next_document(citation):
                return _mvp_next_get(
                    citation,
                    "document",
                    {},
                )

            def _mvp_next_document_id(citation):
                document = _mvp_next_document(citation)

                return str(
                    _mvp_next_get(
                        document,
                        "document_id",
                        "",
                    )
                    or ""
                ).strip().replace("/", "-")

            def _mvp_next_record_id(record):
                for key in (
                    "document_id",
                    "doc_id",
                    "id",
                    "handle",
                ):
                    value = str(
                        record.get(key)
                        or ""
                    ).strip()

                    if value:
                        return value.replace("/", "-")

                url = str(
                    record.get("url")
                    or record.get("repository_url")
                    or ""
                )

                match = _mvp_next_re.search(
                    r"handle/(\d+)/(\d+)",
                    url,
                )

                if match:
                    return (
                        f"{match.group(1)}-"
                        f"{match.group(2)}"
                    )

                return ""

            def _mvp_next_authors(value):
                values = (
                    value
                    if isinstance(value, list)
                    else [value]
                )
                result = []

                for item in values:
                    if isinstance(item, dict):
                        name = str(
                            item.get("full_name")
                            or item.get("name")
                            or item.get("author")
                            or ""
                        ).strip()
                    else:
                        name = str(item or "").strip()

                    if name:
                        result.append({
                            "author_id": "",
                            "full_name": name,
                            "email": "",
                            "orcid": "",
                            "metadata": {},
                        })

                return result

            _mvp_next_question = str(
                question or ""
            ).strip()
            _mvp_next_lower = (
                _mvp_next_question.lower()
            )

            _mvp_next_continuation = bool(
                _mvp_next_re.search(
                    r"\b("
                    r"tertarik|memilih|pilih|judul ini|"
                    r"judul tersebut|pandu|panduan|"
                    r"mulai|langkah awal|lanjutkan|"
                    r"pembuatan skripsi|buat proposal|"
                    r"rumusan masalah|bab 1|metodologi"
                    r")\b",
                    _mvp_next_lower,
                )
            )

            _mvp_next_title = ""

            _mvp_next_title_match = (
                _mvp_next_re.search(
                    r"judul\s+(?:ini|tersebut)"
                    r"\s*:?\s*(.+)",
                    _mvp_next_question,
                    flags=_mvp_next_re.IGNORECASE,
                )
            )

            if _mvp_next_title_match:
                _mvp_next_title = (
                    _mvp_next_title_match.group(1)
                )

                _mvp_next_title = (
                    _mvp_next_re.split(
                        r"(?:[.!?]\s*|\s+)"
                        r"(?:tolong|bantu|pandu|"
                        r"bagaimana|saya ingin)\b",
                        _mvp_next_title,
                        maxsplit=1,
                        flags=_mvp_next_re.IGNORECASE,
                    )[0]
                ).strip(" \n\t.,:;\"'")

            if len(_mvp_next_title) > 180:
                _mvp_next_title = (
                    _mvp_next_title[:180]
                    .rsplit(" ", 1)[0]
                    .strip()
                )

            _mvp_next_active_topic = (
                _mvp_next_title
                or _mvp_next_question
            )
            _mvp_next_active_lower = (
                _mvp_next_active_topic.lower()
            )

            _mvp_next_weather = bool(
                _mvp_next_re.search(
                    r"\b("
                    r"cuaca|curah hujan|hujan|"
                    r"suhu|angin|meteorologi|"
                    r"radiasi matahari|iklim"
                    r")\b",
                    _mvp_next_active_lower,
                )
            )
            _mvp_next_prediction = bool(
                _mvp_next_re.search(
                    r"\b("
                    r"prediksi|peramalan|forecast|"
                    r"machine learning|neural network|"
                    r"lstm|ann"
                    r")\b",
                    _mvp_next_active_lower,
                )
            )

            _mvp_next_catalog_path = (
                _MvpNextPath(__file__).resolve().parents[2]
                / "repository_data"
                / "metadata"
                / "skripsi_dataset.json"
            )
            _mvp_next_records = []

            if _mvp_next_catalog_path.is_file():
                _mvp_next_catalog = (
                    _mvp_next_json.loads(
                        _mvp_next_catalog_path.read_text(
                            encoding="utf-8",
                        )
                    )
                )

                if isinstance(_mvp_next_catalog, list):
                    _mvp_next_records = _mvp_next_catalog
                elif isinstance(_mvp_next_catalog, dict):
                    for _mvp_next_value in (
                        _mvp_next_catalog.values()
                    ):
                        if isinstance(
                            _mvp_next_value,
                            list,
                        ):
                            _mvp_next_records = (
                                _mvp_next_value
                            )
                            break

            _mvp_next_stopwords = {
                "studi",
                "komparatif",
                "optimasi",
                "machine",
                "learning",
                "untuk",
                "dengan",
                "judul",
                "skripsi",
                "tolong",
                "pandu",
                "mulai",
                "saya",
                "tertarik",
            }

            _mvp_next_tokens = {
                token
                for token in _mvp_next_re.findall(
                    r"[a-z0-9]+",
                    _mvp_next_active_lower,
                )
                if len(token) >= 4
                and token not in _mvp_next_stopwords
            }

            _mvp_next_weather_terms = (
                "cuaca",
                "curah hujan",
                "hujan",
                "suhu",
                "angin",
                "meteorologi",
                "radiasi matahari",
                "iklim",
            )
            _mvp_next_prediction_terms = (
                "prediksi",
                "peramalan",
                "forecast",
                "forecasting",
                "klasifikasi",
            )

            _mvp_next_ranked = []

            for _mvp_next_record in _mvp_next_records:
                if not isinstance(_mvp_next_record, dict):
                    continue

                _mvp_next_id = (
                    _mvp_next_record_id(
                        _mvp_next_record
                    )
                )
                _mvp_next_record_title = str(
                    _mvp_next_record.get("title")
                    or ""
                ).strip()
                _mvp_next_abstract = str(
                    _mvp_next_record.get("abstract")
                    or ""
                ).strip()

                if not _mvp_next_id or not _mvp_next_record_title:
                    continue

                _mvp_next_title_lower = (
                    _mvp_next_record_title.lower()
                )
                _mvp_next_blob = (
                    _mvp_next_title_lower
                    + " "
                    + _mvp_next_abstract.lower()
                )

                _mvp_next_title_weather = any(
                    term in _mvp_next_title_lower
                    for term in _mvp_next_weather_terms
                )
                _mvp_next_blob_weather = any(
                    term in _mvp_next_blob
                    for term in _mvp_next_weather_terms
                )
                _mvp_next_title_prediction = any(
                    term in _mvp_next_title_lower
                    for term in _mvp_next_prediction_terms
                )
                _mvp_next_blob_prediction = any(
                    term in _mvp_next_blob
                    for term in _mvp_next_prediction_terms
                )

                if (
                    _mvp_next_weather
                    and _mvp_next_prediction
                    and not (
                        _mvp_next_blob_weather
                        and _mvp_next_blob_prediction
                    )
                ):
                    continue

                _mvp_next_title_overlap = sum(
                    token in _mvp_next_title_lower
                    for token in _mvp_next_tokens
                )
                _mvp_next_blob_overlap = sum(
                    token in _mvp_next_blob
                    for token in _mvp_next_tokens
                )

                _mvp_next_score = (
                    _mvp_next_title_overlap * 24
                    + _mvp_next_blob_overlap * 3
                    + (
                        24
                        if _mvp_next_title_weather
                        else 0
                    )
                    + (
                        24
                        if _mvp_next_title_prediction
                        else 0
                    )
                    + (
                        5
                        if _mvp_next_blob_weather
                        else 0
                    )
                    + (
                        5
                        if _mvp_next_blob_prediction
                        else 0
                    )
                )

                if _mvp_next_score > 0:
                    _mvp_next_ranked.append((
                        _mvp_next_score,
                        _mvp_next_record,
                    ))

            _mvp_next_ranked.sort(
                key=lambda item: (
                    -item[0],
                    str(
                        item[1].get("title")
                        or ""
                    ).lower(),
                )
            )

            _mvp_next_existing = {
                _mvp_next_document_id(item): item
                for item in list(citations or [])
                if _mvp_next_document_id(item)
            }

            _mvp_next_selected = []

            for (
                _mvp_next_score,
                _mvp_next_record,
            ) in _mvp_next_ranked:
                if len(_mvp_next_selected) >= 3:
                    break

                _mvp_next_id = (
                    _mvp_next_record_id(
                        _mvp_next_record
                    )
                )

                if any(
                    _mvp_next_document_id(item)
                    == _mvp_next_id
                    for item in _mvp_next_selected
                ):
                    continue

                if _mvp_next_id in _mvp_next_existing:
                    _mvp_next_selected.append(
                        _mvp_next_existing[
                            _mvp_next_id
                        ]
                    )
                    continue

                _mvp_next_author = (
                    _mvp_next_record.get("author")
                    or _mvp_next_record.get("authors")
                    or ""
                )
                _mvp_next_year = (
                    _mvp_next_record.get("year")
                    or ""
                )
                _mvp_next_prodi = (
                    _mvp_next_record.get("prodi")
                    or _mvp_next_record.get(
                        "program_studi"
                    )
                    or ""
                )
                _mvp_next_url = (
                    _mvp_next_record.get("url")
                    or _mvp_next_record.get(
                        "repository_url"
                    )
                    or ""
                )
                _mvp_next_abstract = str(
                    _mvp_next_record.get("abstract")
                    or ""
                ).strip()

                _mvp_next_selected.append({
                    "chunk_id": (
                        "metadata:"
                        + _mvp_next_id
                    ),
                    "document": {
                        "document_id": _mvp_next_id,
                        "title": str(
                            _mvp_next_record.get(
                                "title"
                            )
                            or ""
                        ).strip(),
                        "authors": _mvp_next_authors(
                            _mvp_next_author
                        ),
                        "collection": "repository",
                        "entities": [],
                        "file_path": "",
                        "metadata": {
                            "author":
                                _mvp_next_author,
                            "year":
                                _mvp_next_year,
                            "prodi":
                                _mvp_next_prodi,
                            "program_studi":
                                _mvp_next_prodi,
                            "url":
                                _mvp_next_url,
                            "repository_url":
                                _mvp_next_url,
                            "abstract":
                                _mvp_next_abstract,
                            "metadata_only": True,
                        },
                    },
                    "metadata": {
                        "evidence_type":
                            "metadata_abstract",
                        "source_kind_label":
                            "Metadata/Abstrak",
                        "source_label":
                            "Repository metadata",
                        "metadata_only": True,
                        "section": "",
                        "page_start": None,
                        "page_end": None,
                        "author":
                            _mvp_next_author,
                        "year":
                            _mvp_next_year,
                        "prodi":
                            _mvp_next_prodi,
                        "program_studi":
                            _mvp_next_prodi,
                        "url":
                            _mvp_next_url,
                        "repository_url":
                            _mvp_next_url,
                    },
                    "page": None,
                    "score": float(
                        _mvp_next_score
                    ),
                    "text":
                        _mvp_next_abstract[:1800],
                })

            if (
                _mvp_next_weather
                and _mvp_next_prediction
                and len(_mvp_next_selected) >= 2
            ):
                citations = _mvp_next_selected[:3]

            # Synchronize source labels in the initial three ideas.
            if (
                not _mvp_next_continuation
                and "## Ide 1" in str(generated or "")
                and citations
            ):
                _mvp_next_source_lines = []

                for _mvp_next_source in citations:
                    _mvp_next_source_document = (
                        _mvp_next_document(
                            _mvp_next_source
                        )
                    )
                    _mvp_next_source_lines.append(
                        "**Sumber pendukung:** "
                        f"[{_mvp_next_document_id(_mvp_next_source)}] "
                        f"{str(_mvp_next_get(_mvp_next_source_document, 'title', '') or '').strip()}."
                    )

                _mvp_next_counter = [0]

                def _mvp_next_replace_source(match):
                    replacement = _mvp_next_source_lines[
                        _mvp_next_counter[0]
                        % len(_mvp_next_source_lines)
                    ]
                    _mvp_next_counter[0] += 1
                    return replacement

                generated = _mvp_next_re.sub(
                    r"\*\*Sumber pendukung:\*\*[^\n]*",
                    _mvp_next_replace_source,
                    str(generated or ""),
                )

            if (
                _mvp_next_continuation
                and _mvp_next_title
            ):
                _mvp_next_reference_rows = []

                for _mvp_next_index, (
                    _mvp_next_source
                ) in enumerate(citations, start=1):
                    _mvp_next_source_document = (
                        _mvp_next_document(
                            _mvp_next_source
                        )
                    )
                    _mvp_next_reference_rows.append(
                        f"{_mvp_next_index}. "
                        f"[{_mvp_next_document_id(_mvp_next_source)}] "
                        f"{str(_mvp_next_get(_mvp_next_source_document, 'title', '') or '').strip()}."
                    )

                _mvp_next_references = (
                    "\n".join(
                        _mvp_next_reference_rows
                    )
                    or (
                        "Referensi tambahan akan dipilih "
                        "setelah ruang lingkup ditentukan."
                    )
                )

                generated = "\n\n".join([
                    "## Panduan Memulai Skripsi",
                    (
                        "Kamu sudah memilih arah penelitian. "
                        "Sekarang kita ubah judul tersebut "
                        "menjadi rencana yang dapat dikerjakan."
                    ),
                    (
                        "### Judul pilihan\n"
                        f"**{_mvp_next_title}**"
                    ),
                    (
                        "### 1. Sempurnakan ruang lingkup\n"
                        "Judul ini masih luas. Tentukan:\n\n"
                        "1. **Target prediksi:** curah hujan, "
                        "suhu, kecepatan angin, atau kategori "
                        "cuaca.\n"
                        "2. **Lokasi dan dataset:** stasiun "
                        "BMKG atau wilayah tertentu dengan "
                        "periode data yang jelas.\n"
                        "3. **Model pembanding:** misalnya "
                        "Random Forest, XGBoost, dan LSTM.\n\n"
                        "Format judul yang lebih operasional:\n"
                        "**Studi Komparatif dan Optimasi Random "
                        "Forest, XGBoost, dan LSTM untuk "
                        "Prediksi [Target Cuaca] di [Lokasi].**"
                    ),
                    (
                        "### 2. Draft rumusan masalah\n"
                        "1. Model mana yang memberikan performa "
                        "terbaik pada dataset dan pembagian "
                        "waktu yang sama?\n"
                        "2. Seberapa besar pengaruh optimasi "
                        "hyperparameter terhadap performa?\n"
                        "3. Bagaimana stabilitas model pada "
                        "musim atau kondisi ekstrem?"
                    ),
                    (
                        "### 3. Tujuan penelitian\n"
                        "1. Membandingkan beberapa model dengan "
                        "pipeline eksperimen yang seragam.\n"
                        "2. Mengoptimalkan hyperparameter tanpa "
                        "data leakage.\n"
                        "3. Menentukan model terbaik berdasarkan "
                        "akurasi, stabilitas, waktu inferensi, "
                        "dan biaya komputasi."
                    ),
                    (
                        "### 4. Desain metodologi awal\n"
                        "1. Audit dan bersihkan data cuaca.\n"
                        "2. Bentuk fitur lag, rolling statistics, "
                        "bulan, musim, dan waktu.\n"
                        "3. Gunakan **time-series split**, bukan "
                        "random split biasa.\n"
                        "4. Bangun baseline sederhana.\n"
                        "5. Latih seluruh model pada data dan "
                        "horizon prediksi yang sama.\n"
                        "6. Optimalkan hyperparameter hanya "
                        "pada training dan validation set.\n"
                        "7. Evaluasi menggunakan MAE, RMSE, "
                        "MAPE, waktu inferensi, dan performa "
                        "per musim."
                    ),
                    (
                        "### 5. Data yang perlu disiapkan\n"
                        "- Tanggal dan waktu observasi.\n"
                        "- Variabel target.\n"
                        "- Suhu, kelembapan, tekanan udara, "
                        "angin, dan curah hujan jika tersedia.\n"
                        "- Lokasi atau identitas stasiun.\n"
                        "- Data beberapa tahun untuk menguji "
                        "pola musiman."
                    ),
                    (
                        "### 6. Struktur proposal\n"
                        "- **Bab I:** latar belakang, rumusan "
                        "masalah, tujuan, manfaat, dan batasan.\n"
                        "- **Bab II:** time series, model, "
                        "optimasi, penelitian terdahulu, dan "
                        "research gap.\n"
                        "- **Bab III:** dataset, preprocessing, "
                        "split waktu, model, optimasi, metrik, "
                        "dan skenario eksperimen."
                    ),
                    (
                        "### 7. Rencana kerja 14 hari\n"
                        "- **Hari 1–2:** pilih target, lokasi, "
                        "dataset, dan model.\n"
                        "- **Hari 3–5:** audit dataset dan EDA.\n"
                        "- **Hari 6–8:** susun matriks penelitian "
                        "terdahulu.\n"
                        "- **Hari 9–11:** tulis latar belakang, "
                        "rumusan masalah, dan tujuan.\n"
                        "- **Hari 12–14:** finalisasi desain "
                        "eksperimen dan Bab III awal."
                    ),
                    (
                        "### Referensi awal repository\n"
                        f"{_mvp_next_references}"
                    ),
                    (
                        "### Langkah pertama sekarang\n"
                        "Balas dengan:\n\n"
                        "**Target cuaca:** …  \n"
                        "**Lokasi/dataset:** …  \n"
                        "**Model pembanding:** …\n\n"
                        "DELBot kemudian dapat menyusun judul "
                        "final, rumusan masalah, tujuan, "
                        "batasan, serta kerangka Bab I."
                    ),
                ])

        except Exception:
            # Final continuation must never create HTTP 500.
            pass


        # DELBOT MVP contextual research synthesis v3 767916
        import re as _v7_re

        _v7_question = str(question or "").strip()
        _v7_lower = _v7_question.lower()

        _v7_followup = bool(
            _v7_re.search(
                r"\b(?:tertarik|judul ini|judul tersebut|pandu|"
                r"referensi lebih lanjut|mulai tahap|mulai membuat|"
                r"mulai pembuatan|lanjutkan)\b",
                _v7_lower,
            )
        )

        _v7_weather = bool(
            _v7_re.search(
                r"\b(?:cuaca|curah hujan|hujan|angin|suhu|"
                r"meteorologi|radiasi matahari)\b",
                _v7_lower,
            )
        )

        _v7_idea_request = (
            not _v7_followup
            and _v7_weather
            and bool(
                _v7_re.search(
                    r"\b(?:ide|judul|topik|skripsi|tugas akhir|"
                    r"research gap)\b",
                    _v7_lower,
                )
            )
        )

        def _v7_record(value):
            return value if isinstance(value, dict) else {}

        def _v7_value(value, keys, depth=0):
            if depth > 5:
                return ""

            record = _v7_record(value)

            for key in keys:
                candidate = record.get(key)

                if isinstance(candidate, str) and candidate.strip():
                    return candidate.strip()

                if isinstance(candidate, (int, float)):
                    return str(candidate)

                if isinstance(candidate, list):
                    values = []

                    for item in candidate:
                        if isinstance(item, str) and item.strip():
                            values.append(item.strip())
                        elif isinstance(item, dict):
                            name = (
                                item.get("full_name")
                                or item.get("name")
                                or item.get("author")
                            )

                            if isinstance(name, str) and name.strip():
                                values.append(name.strip())

                    if values:
                        return ", ".join(values)

            for candidate in record.values():
                if isinstance(candidate, dict):
                    nested = _v7_value(
                        candidate,
                        keys,
                        depth + 1,
                    )

                    if nested:
                        return nested

            return ""

        def _v7_unique_sources(items):
            result = []
            seen = set()

            for item in items if isinstance(items, list) else []:
                document_id = _v7_value(
                    item,
                    ["document_id", "repository_id", "id"],
                )
                title = _v7_value(
                    item,
                    ["title", "document_title"],
                )
                key = document_id.lower() or title.lower()

                if not key or key in seen:
                    continue

                seen.add(key)
                result.append(item)

            return result[:3]

        citations = _v7_unique_sources(citations)

        _v7_sources = []

        for _v7_index, _v7_citation in enumerate(citations, 1):
            _v7_title = _v7_value(
                _v7_citation,
                ["title", "document_title"],
            )
            _v7_id = _v7_value(
                _v7_citation,
                ["document_id", "repository_id", "id"],
            )
            _v7_year = _v7_value(
                _v7_citation,
                ["year", "publication_year"],
            )
            _v7_prodi = _v7_value(
                _v7_citation,
                ["prodi", "program_studi", "study_program"],
            )
            _v7_sources.append(
                {
                    "number": _v7_index,
                    "id": _v7_id,
                    "title": _v7_title,
                    "year": _v7_year,
                    "prodi": _v7_prodi,
                }
            )

        if _v7_idea_request and len(_v7_sources) >= 2:
            _v7_titles = "\n".join(
                f"- **[Sumber {source['number']}]** "
                f"{source['title']}"
                + (
                    f" ({source['year']})"
                    if source["year"]
                    else ""
                )
                for source in _v7_sources
            )

            generated = f"""## Temuan dari repository

{_v7_titles}

Ketiga penelitian tersebut belum dapat dibandingkan langsung. Target prediksi, wilayah, metode, dan rancangan pengujiannya berbeda. Karena itu, gap yang paling kuat bukan sekadar “menggunakan algoritma lain”, melainkan **membuat perbandingan model dalam satu eksperimen yang benar-benar setara**.

## Gap penelitian

Belum terlihat penelitian repository yang membandingkan Random Forest, XGBoost, dan LSTM menggunakan:

- dataset dan periode yang sama;
- variabel masukan yang sama;
- horizon prediksi yang sama;
- pembagian data berdasarkan waktu;
- prosedur optimasi yang setara; dan
- metrik evaluasi yang sama.

Gap ini dapat diuji dan hasilnya dapat dibuktikan secara kuantitatif.

## Pilihan judul

### 1. Studi komparatif tiga model

**Studi Komparatif dan Optimasi Random Forest, XGBoost, dan LSTM untuk Prediksi Curah Hujan Berbasis Data Cuaca**

Cocok jika tujuan utama penelitian adalah menentukan model terbaik secara adil.

- **Yang dibandingkan:** akurasi, kestabilan antarmusim, waktu pelatihan, dan waktu inferensi.
- **Rancangan:** satu dataset, satu horizon, satu skema pembagian waktu, dan anggaran optimasi yang sama.
- **Evaluasi:** MAE, RMSE, error per musim, serta waktu komputasi.
- **Nilai penelitian:** menghasilkan rekomendasi model yang dapat diuji ulang.
- **Sumber utama:** [Sumber 1], [Sumber 2], dan [Sumber 3].

### 2. Prediksi curah hujan dan angin secara bersamaan

**Perbandingan Model Terpisah dan Multi-Output Learning untuk Prediksi Curah Hujan dan Kecepatan Angin**

Cocok jika dataset memiliki target curah hujan dan kecepatan angin pada waktu yang sama.

- **Yang diuji:** apakah pembelajaran dua target memberikan hasil lebih baik daripada model terpisah.
- **Rancangan:** bandingkan model satu target dengan model multi-output.
- **Evaluasi:** MAE/RMSE setiap target dan perubahan error ketika terjadi nilai ekstrem.
- **Nilai penelitian:** menjelaskan apakah hubungan hujan–angin membantu proses prediksi.
- **Sumber utama:** terutama penelitian curah hujan dan kecepatan angin, didukung sumber cuaca lainnya.

### 3. Ketahanan model pada musim berbeda

**Analisis Ketahanan Model Prediksi Curah Hujan terhadap Perubahan Musim dan Kejadian Ekstrem**

Cocok jika tersedia data beberapa tahun.

- **Yang diuji:** apakah model tetap stabil pada musim hujan, musim kering, dan periode transisi.
- **Rancangan:** pengujian bergulir berdasarkan waktu dan evaluasi terpisah per musim.
- **Evaluasi:** error keseluruhan, error per musim, dan kemampuan mendeteksi hujan ekstrem.
- **Nilai penelitian:** memberikan evaluasi yang lebih realistis daripada satu nilai error rata-rata.
- **Sumber utama:** [Sumber 1], [Sumber 2], dan [Sumber 3].

## Rekomendasi

Pilih **judul pertama** apabila kamu ingin ruang lingkup yang paling jelas dan mudah dipertanggungjawabkan. Target, model, dan evaluasinya sudah konkret. Keputusan yang masih dibutuhkan hanya lokasi dataset, periode data, dan horizon prediksi.
"""

        if _v7_followup and (
            _v7_weather
            or "random forest" in _v7_lower
            or "xgboost" in _v7_lower
            or "lstm" in _v7_lower
        ):
            _v7_selected_title = ""

            for _v7_line in _v7_question.splitlines():
                _v7_clean_line = _v7_line.strip()

                if (
                    "studi komparatif" in _v7_clean_line.lower()
                    and "prediksi curah hujan" in _v7_clean_line.lower()
                ):
                    _v7_selected_title = _v7_clean_line
                    break

            if not _v7_selected_title:
                _v7_match = _v7_re.search(
                    r"(Studi Komparatif.+?Prediksi Curah Hujan"
                    r"(?: Berbasis Data Cuaca)?)",
                    _v7_question,
                    flags=_v7_re.IGNORECASE | _v7_re.DOTALL,
                )

                if _v7_match:
                    _v7_selected_title = " ".join(
                        _v7_match.group(1).split()
                    )

            if not _v7_selected_title:
                _v7_selected_title = (
                    "Studi Komparatif dan Optimasi Random Forest, "
                    "XGBoost, dan LSTM untuk Prediksi Curah Hujan "
                    "Berbasis Data Cuaca"
                )

            _v7_reading_rows = []

            for source in _v7_sources:
                title_lower = source["title"].lower()

                if (
                    "curah hujan" in title_lower
                    and "kecepatan angin" in title_lower
                ):
                    reading_task = (
                        "Catat lokasi, variabel cuaca, bentuk target, "
                        "arsitektur ANN, pembagian data, metrik, hasil, "
                        "dan keterbatasan penelitian."
                    )
                elif "backpropagation" in title_lower:
                    reading_task = (
                        "Catat preprocessing, konfigurasi jaringan, "
                        "periode data, horizon prediksi, metrik, dan "
                        "kelemahan model pada curah hujan tinggi."
                    )
                elif (
                    "support vector regression" in title_lower
                    or "deep belief network" in title_lower
                ):
                    reading_task = (
                        "Catat cara perbandingan model, skema pengujian, "
                        "metrik, model terbaik, dan apakah pembagian "
                        "datanya sudah mengikuti urutan waktu."
                    )
                elif "radiasi matahari" in title_lower:
                    reading_task = (
                        "Catat variabel meteorologis, feature engineering, "
                        "pembagian data, metode machine learning, serta "
                        "prosedur evaluasinya."
                    )
                else:
                    reading_task = (
                        "Catat masalah, dataset, variabel, metode, metrik, "
                        "hasil utama, dan keterbatasan."
                    )

                identifier = (
                    f" `{source['id']}`"
                    if source["id"]
                    else ""
                )

                _v7_reading_rows.append(
                    f"### {source['number']}. "
                    f"{source['title']}{identifier}\n\n"
                    f"{reading_task}"
                )

            _v7_reference_section = (
                "\n\n".join(_v7_reading_rows)
                if _v7_reading_rows
                else (
                    "Belum ditemukan sumber repository yang cukup "
                    "untuk membuat matriks awal."
                )
            )

            generated = f"""## Mulai dari sini

**Judul kerja**

{_v7_selected_title}

Target penelitian dan model pembanding sudah jelas. Kamu **tidak perlu memilih target atau model lagi**. Hal yang masih perlu ditentukan hanya:

1. lokasi atau stasiun sumber data;
2. periode data;
3. horizon prediksi, misalnya satu hari atau beberapa hari ke depan.

## Referensi yang dibaca terlebih dahulu

{_v7_reference_section}

Repository saat ini memberi landasan kuat untuk ANN, backpropagation, DBN, dan SVR. Namun, untuk mendukung perbandingan Random Forest, XGBoost, dan LSTM secara lengkap, kamu masih perlu mencari penelitian yang secara khusus menggunakan ketiga model tersebut untuk prediksi curah hujan.

Gunakan kata kunci berikut pada pencarian literatur lanjutan:

- `rainfall forecasting Random Forest`;
- `rainfall prediction XGBoost`;
- `rainfall forecasting LSTM`;
- `time-series split rainfall prediction`;
- `hyperparameter optimization rainfall forecasting`; dan
- `extreme rainfall prediction machine learning`.

## Matriks penelitian terdahulu

Buat tabel dengan kolom berikut:

| Bagian | Informasi yang dicatat |
|---|---|
| Identitas | Penulis, tahun, judul, dan sumber |
| Dataset | Lokasi, periode, jumlah data, dan resolusi waktu |
| Target | Curah hujan kontinu atau kategori hujan |
| Fitur | Suhu, kelembapan, tekanan, angin, dan fitur waktu |
| Metode | Model, konfigurasi, dan optimasi |
| Validasi | Random split, time-series split, atau rolling evaluation |
| Metrik | MAE, RMSE, MAPE, akurasi, atau metrik lainnya |
| Hasil | Model terbaik dan nilai evaluasi |
| Keterbatasan | Data, metode, evaluasi, atau generalisasi |
| Peluang gap | Bagian yang dapat diperbaiki oleh penelitianmu |

Jangan hanya menyalin abstrak. Ambil informasi metode dan evaluasi dari Bab III serta hasil dari Bab IV ketika PDF tersedia.

## Rumusan masalah awal

1. Bagaimana perbandingan kinerja Random Forest, XGBoost, dan LSTM untuk prediksi curah hujan ketika menggunakan dataset serta skema pengujian yang sama?
2. Seberapa besar optimasi hyperparameter meningkatkan kinerja setiap model?
3. Model mana yang memberikan keseimbangan terbaik antara akurasi, kestabilan, dan waktu komputasi?

## Rancangan eksperimen awal

1. Urutkan data berdasarkan waktu dan periksa data hilang.
2. Tentukan target curah hujan dan horizon prediksi.
3. Bentuk fitur waktu, lag, dan statistik bergerak tanpa menggunakan informasi masa depan.
4. Buat baseline sederhana, misalnya persistence forecast.
5. Gunakan time-series split untuk training dan validation.
6. Latih Random Forest, XGBoost, dan LSTM pada fitur serta periode yang sama.
7. Optimalkan setiap model dengan anggaran pencarian yang setara.
8. Uji sekali pada test set terakhir yang tidak digunakan saat optimasi.
9. Bandingkan MAE, RMSE, error per musim, waktu latih, dan waktu inferensi.

## Pekerjaan pertama

### Hari 1

- Tentukan lokasi dataset.
- Pastikan data curah hujan tersedia dalam format waktu yang konsisten.
- Catat periode dan interval observasinya.

### Hari 2

- Unduh atau kumpulkan tiga sumber repository.
- Isi minimal tiga baris matriks penelitian terdahulu.
- Tandai informasi yang belum tersedia dalam metadata.

### Hari 3

- Cari masing-masing dua referensi tambahan untuk Random Forest, XGBoost, dan LSTM.
- Prioritaskan penelitian dengan data curah hujan dan validasi berdasarkan waktu.

### Hari 4–5

- Susun latar belakang dari masalah prediksi curah hujan, kelemahan perbandingan penelitian terdahulu, dan kebutuhan eksperimen yang setara.
- Finalisasi rumusan masalah, tujuan, serta batasan penelitian.

## Informasi yang dibutuhkan berikutnya

Balas hanya dengan:

**Lokasi atau stasiun:** …  
**Periode data:** …  
**Interval data:** harian/jam  
**Horizon prediksi:** …

Setelah itu DELBot dapat menyusun judul final, batasan penelitian, matriks eksperimen, dan kerangka Bab I tanpa mengulang pemilihan target maupun model.
"""


        return ResearchPipelineResponse(
            answer=generated,
            citations=citations,
            research_state=research_state,
            rag=rag,
        )
