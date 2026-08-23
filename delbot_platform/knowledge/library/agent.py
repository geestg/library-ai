from __future__ import annotations

import re
from typing import Dict, List, Any

from delbot_platform.knowledge.library.parser import LibraryParser
from delbot_platform.knowledge.library.tools import LibraryAcademicTools
from delbot_platform.knowledge.library.academic import route_intent, AcademicIntentHandlers


class LibraryAcademicAgent:
    """
    LibraryAcademicAgent bertindak sebagai agen otonom akademik (DELBot) untuk civitas akademika IT Del.
    Membantu mencari buku katalog, rekomendasi, status rak, dan menjawab FAQ umum perpustakaan.
    """
    def __init__(self):
        self.parser = LibraryParser()
        self.tools = LibraryAcademicTools()
        self.handlers = AcademicIntentHandlers(self.tools)

    def _route_intent(self, query: str) -> str:
        return route_intent(query, self.tools.faq_tool)

    def run(self, query: str, history: List[Dict[str, str]] = None, current_time: str = None, user_role: str = "student") -> Dict[str, Any]:
        """
        EntryPoint Utama eksekusi Agent.
        Mengkoordinasikan memori riwayat chat, pendeteksian intent, ekstraksi parameter,
        pemanggilan tool, dan penyusunan respon.
        """
        if history is None:
            history = []

        query_clean = query.strip()
        if not query_clean:
            return {
                "intent": "faq",
                "response": "Ada yang bisa saya bantu terkait koleksi buku perpustakaan hari ini?",
                "sources": [],
                "citations": []
            }

        # 1. Deteksi Awal 
        initial_intent = self._route_intent(query_clean)
        
        # Cek apakah kueri adalah Multi-Intent (FAQ + Cari Buku)
        EXPLICIT_BOOK_SEARCH_TRIGGERS = ["cari buku", "carikan buku", "rekomendasi buku", "rekomendasikan buku", "referensi buku", "buku tentang", "buku untuk"]
        is_multi_intent = False
        if initial_intent == "faq":
            if any(trig in query_clean.lower() for trig in EXPLICIT_BOOK_SEARCH_TRIGGERS):
                is_multi_intent = True

        if initial_intent == "faq" and not is_multi_intent:
            return self.handlers.handle_faq(query_clean, current_time=current_time, user_role=user_role, history=history)
            
        # Ambil konteks FAQ jika ini adalah multi-intent
        faq_context = ""
        if is_multi_intent:
            faq_context = self.tools.faq_tool(query_clean) or ""

        # 2. Reformulasi Kueri (Chat Memory) jika riwayat tersedia
        target_query = query_clean

        # 3. Ekstraksi Metadata / Parameter Pencarian
        metadata_filter = self.parser.parse(target_query)

        # 4. Tentukan Intent Akhir dari kueri target yang sudah dirumuskan ulang
        intent = "recommendation" if is_multi_intent else self._route_intent(target_query)

        # 5. Jalankan Aksi/Tool Agen sesuai Intent
        if intent == "status":
            return self.handlers.handle_status_or_location(target_query, metadata_filter)
        else:
            return self.handlers.handle_recommendation(target_query, metadata_filter, history=history, faq_context=faq_context)
