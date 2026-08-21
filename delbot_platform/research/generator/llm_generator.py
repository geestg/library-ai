from __future__ import annotations

import re

from delbot_platform.ai.client.llm_client import LLMClient


class LLMGenerator:
    """
    MVP LLM answer generator.

    Normal generation is followed by one clean synthesis pass when
    the model copies context or produces an oversized answer.

    The repair pass intentionally does NOT resend the previous draft
    or the full internal message stack. It builds a clean request from
    the user question and document evidence only.
    """

    MAX_NORMAL_CHARS = 2500
    MAX_REPAIR_CHARS = 2200
    MAX_EVIDENCE_CHARS = 7000

    def __init__(
        self,
    ) -> None:

        self.client = LLMClient()

    def _needs_repair(
        self,
        answer: str,
    ) -> bool:

        text = str(
            answer or ""
        ).strip()

        needs_repair = False

        if not text:
            needs_repair = True

        if len(text) > self.MAX_NORMAL_CHARS:
            needs_repair = True

        normalized = " ".join(
            text.lower().split()
        )

        generic_prefixes = (
            "berdasarkan dokumen yang ditemukan:",
            "berdasarkan dokumen yang ditemukan",
            "berdasarkan context:",
            "berdasarkan konteks:",
        )

        if any(
            normalized.startswith(prefix)
            for prefix in generic_prefixes
        ):
            needs_repair = True

        repeated_source_patterns = (
            r"\bBAB\s+[IVXLC]+\b",
            r"\bInstitut Teknologi Del\b",
            r"\bStudi Literatur\b.*\bPerumusan Masalah\b",
            r"\bPenyusunan Kuesioner\b.*\bPenyebaran Kuesioner\b",
            r"\bOrientation Script\b.*\bBackground Questionnaire\b",
        )

        matches = 0

        for pattern in repeated_source_patterns:
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.DOTALL,
            ):
                matches += 1

        if matches >= 1:
            needs_repair = True

        repair_markers = (
            "Gunakan context di atas",
            "Jangan menyalinnya kembali",
            "DOCUMENT CONTEXT",
            "CURRENT RESEARCH STATE",
            "FINAL ANSWER INSTRUCTION",
            "ANSWER REPAIR MODE",
        )

        marker_hits = 0

        for marker in repair_markers:
            if marker.lower() in text.lower():
                marker_hits += 1

        if marker_hits >= 1:
            needs_repair = True

        return needs_repair

    def _extract_user_question(
        self,
        messages: list[dict],
    ) -> str:

        question = ""

        for message in reversed(messages):
            role = str(
                message.get("role", "")
            ).lower()

            content = str(
                message.get("content", "")
            ).strip()

            if role == "user" and content:
                question = content
                break

        if not question:
            question = "Jawab pertanyaan pengguna berdasarkan evidence."

        if len(question) > 1000:
            question = question[:1000].strip()

        return question

    def _extract_document_context(
        self,
        messages: list[dict],
    ) -> str:

        context = ""

        for message in messages:
            content = str(
                message.get("content", "")
            )

            if "DOCUMENT CONTEXT" in content:
                marker = "DOCUMENT CONTEXT"
                start = content.find(marker)

                if start >= 0:
                    context = content[start:]
                    break

        if not context:
            for message in messages:
                content = str(
                    message.get("content", "")
                )

                if "[SOURCE " in content:
                    context = content
                    break

        context = context.strip()

        if len(context) > self.MAX_EVIDENCE_CHARS:
            context = context[:self.MAX_EVIDENCE_CHARS].rstrip()

        return context

    def _build_clean_repair_messages(
        self,
        messages: list[dict],
    ) -> list[dict]:

        question = self._extract_user_question(
            messages,
        )

        evidence = self._extract_document_context(
            messages,
        )

        clean_system = (
            "Anda adalah DELBot, AI Research Assistant akademik.\n\n"
            "Tugas Anda adalah menjawab pertanyaan pengguna berdasarkan "
            "evidence dokumen yang diberikan.\n\n"
            "ATURAN WAJIB:\n"
            "1. Jawab pertanyaan pengguna secara langsung.\n"
            "2. Gunakan hanya evidence yang tersedia.\n"
            "3. Jangan menggunakan pengetahuan di luar evidence.\n"
            "4. Jangan menyalin kalimat evidence secara berurutan.\n"
            "5. Jangan menampilkan nama dokumen, nomor halaman, daftar isi, "
            "atau metadata kecuali diperlukan untuk menjawab.\n"
            "6. Jangan memulai dengan 'Berdasarkan dokumen yang ditemukan'.\n"
            "7. Jangan menyebut context, prompt, instruksi internal, atau "
            "proses perbaikan.\n"
            "8. Untuk pertanyaan sederhana, jawab singkat dalam 1-3 paragraf.\n"
            "9. Target sekitar 80-180 kata untuk pertanyaan sederhana.\n"
            "10. Jika evidence tidak cukup untuk menjawab pertanyaan, "
            "katakan dengan jelas bahwa evidence yang tersedia belum cukup.\n"
            "11. Jangan mengisi kekurangan evidence dengan pengetahuan umum.\n"
            "12. Output hanya jawaban final untuk pengguna.\n"
        )

        clean_user = (
            "PERTANYAAN PENGGUNA:\n"
            f"{question}\n\n"
            "EVIDENCE DOKUMEN:\n"
            f"{evidence}\n\n"
            "JAWAB SEKARANG.\n"
            "Jika evidence tidak secara memadai menjawab pertanyaan, "
            "nyatakan keterbatasan evidence secara singkat."
        )

        repaired = [
            {
                "role": "system",
                "content": clean_system,
            },
            {
                "role": "user",
                "content": clean_user,
            },
        ]

        return repaired

    def generate(
        self,
        messages: list[dict],
    ) -> str:

        generated = self.client.chat(
            messages=messages,
        )

        generated = str(
            generated or ""
        ).strip()

        if not self._needs_repair(
            generated,
        ):
            return generated

        repair_messages = (
            self._build_clean_repair_messages(
                messages,
            )
        )

        repaired = self.client.chat(
            messages=repair_messages,
            temperature=0.1,
            max_tokens=300,
        )

        repaired = str(
            repaired or ""
        ).strip()

        if not repaired:
            return generated

        if self._needs_repair(
            repaired,
        ):
            compact_messages = (
                self._build_clean_repair_messages(
                    messages,
                )
            )

            compact_messages[0]["content"] += (
                "\n13. Jawaban harus maksimal 120 kata.\n"
                "14. Jika evidence tidak cukup, cukup katakan evidence "
                "belum cukup untuk menjawab pertanyaan.\n"
            )

            compact = self.client.chat(
                messages=compact_messages,
                temperature=0.0,
                max_tokens=180,
            )

            compact = str(
                compact or ""
            ).strip()

            if compact:
                repaired = compact

        return repaired
