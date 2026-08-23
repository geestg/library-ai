from __future__ import annotations

from typing import Dict, List, Any
from delbot_platform.research.academic_research_engine import research_analysis

class ResearchAgent:
    """
    ResearchAgent bertindak sebagai agen otonom akademik bidang penelitian dan RAG ilmiah.
    Membantu mahasiswa/dosen mencari ide Tugas Akhir (TA), menganalisis research gap,
    melakukan literature review, dan membandingkan metodologi penelitian ilmiah.
    """
    def __init__(self):
        pass

    def run(
        self,
        query: str,
        history: List[Dict[str, str]] = None,
        session_id: str = "",
        active_document_ids: list = [],
        stream: bool = False
    ) -> Any:
        """
        EntryPoint Utama untuk mengeksekusi analisis riset / pencarian ilmiah.
        Mendelegasikan pemrosesan ke research_analysis engine.
        """
        if history is None:
            history = []
            
        return research_analysis(
            query=query,
            session_id=session_id,
            active_document_ids=active_document_ids,
            stream=stream
        )
