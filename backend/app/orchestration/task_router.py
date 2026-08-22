from app.orchestration.intent_classifier import (
    classify_intent
)

from app.orchestration.model_selector import (
    select_model
)


def route_query(query: str, session_id: str = ""):

    # =====================================
    # CHECK SESSION INTENT CONTINUITY
    # If the session has a stored last_intent (e.g. from a prior thesis idea response),
    # use it for follow-up messages that lack clear keyword signals.
    # =====================================
    intent = None
    if session_id:
        try:
            from app.services.research.session import session_manager
            session = session_manager.get_or_create(session_id)
            if session.last_intent:
                # Only inherit last_intent if the current message looks like a follow-up
                # (short message without any direct keyword override)
                followup_signals = [
                    # Ada X lain
                    "ada yang lain", "ada lagi", "ada ide lain", "ada saran lain",
                    "ada topik lain", "ada judul lain", "ada referensi lain",
                    # Saran / ide
                    "saran lain", "saran yang lain", "ide lain", "judul lain",
                    "topik lain", "rekomendasi lain",
                    # Yang lain / lainnya
                    "yang lain", "lainnya", "yang berbeda", "selain itu",
                    # Minta lebih
                    "lebih", "tambah", "tambahkan", "berikan lagi", "kasih lagi",
                    "bisa kasih lagi", "boleh minta lagi", "minta lagi",
                    # Terbaru / menarik
                    "terbaru", "menarik", "yang menarik",
                    # Lanjut
                    "lagi", "lanjut", "lanjutkan", "next", "berikutnya",
                    # Hanya ini?
                    "hanya itu", "itu saja", "cuma itu", "segitu",
                    # English fallback
                    "more", "other", "others", "continue", "another",
                ]
                query_lc = query.lower().strip()

                # Jika kueri adalah pertanyaan penjelasan/saran metode konseptual (bukan minta 5 ide skripsi baru), jangan warisi thesis_idea
                question_explain_signals = [
                    "ada saran metode", "saran metode", "metode lain selain", "selain aiml",
                    "apa bedanya", "mengapa menggunakan", "kenapa menggunakan", "bagaimana cara",
                    "apakah bisa", "mana yang lebih", "penjelasan tentang", "jelaskan", "apa itu"
                ]
                is_question_query = any(q_sig in query_lc for q_sig in question_explain_signals)

                if is_question_query:
                    intent = "general_qa"
                    print(f"[TASK_ROUTER] Conversational question detected — setting intent to 'general_qa'")
                elif any(sig in query_lc for sig in followup_signals):
                    intent = session.last_intent
                    print(f"[TASK_ROUTER] Using session last_intent '{intent}' for follow-up: {query!r}")
        except Exception as e:
            print(f"[TASK_ROUTER] Session intent lookup failed: {e}")

    # =====================================
    # INTENT CLASSIFICATION (fallback)
    # =====================================
    if not intent:
        intent = classify_intent(query)

    # =====================================
    # MODEL SELECTION
    # =====================================
    selected = select_model(intent)

    # =====================================
    # RESPONSE
    # =====================================
    return {
        "intent": intent,
        "provider": selected["provider"],
        "model": selected["model"]
    }
