from __future__ import annotations

from typing import Dict, List, Any, Optional
from delbot_platform.knowledge.library.parser import LibraryParser
from delbot_platform.knowledge.library.retrieval import LibraryRetrieval, RecommendationEngine
from delbot_platform.knowledge.library.faq import answer_faq

class LibraryAcademicTools:
    """
    Kelas penampung tools (perkakas) modular yang digunakan oleh Library Academic Agent.
    Setiap tool merepresentasikan aksi spesifik yang dapat dilakukan agen untuk memecahkan masalah.
    """
    def __init__(self):
        self.parser = LibraryParser()
        self.retrieval = LibraryRetrieval()
        self.recommendation = RecommendationEngine()

    def faq_tool(self, query: str) -> Optional[str]:
        """
        Tool untuk menjawab pertanyaan umum seputar perpustakaan IT Del
        (seperti jam operasional, denda, gedung, dll.) menggunakan irisan token.
        """
        return answer_faq(query)

    def catalog_search_tool(self, query: str, metadata_filter: dict, limit: int = 5) -> List[dict]:
        """
        Tool untuk mencari katalog buku secara hibrida (vector + keyword)
        dan melakukan perankingan ulang (rerank) dengan cross-encoder.
        """
        filter_params = {k: v for k, v in metadata_filter.items() if v}
        return self.recommendation.recommend_by_query(
            query=query,
            limit=limit,
            filter_params=filter_params if filter_params else None
        )

    def physical_location_tool(self, query: str, metadata_filter: dict) -> List[dict]:
        """
        Tool untuk mencari letak fisik rak buku atau lantai berdasarkan pencarian kueri.
        Memiliki mekanisme pembersihan kata henti lokasi agar pencarian tepat pada subjek buku.
        """
        import re
        class_num = metadata_filter.get("classification_number")
        filter_params = {k: v for k, v in metadata_filter.items() if v}
        
        # Bersihkan kata tanya lokasi agar fokus ke subjek buku
        clean_q = re.sub(r'\b(buku|ada|di|rak|lantai|berapa|letak|posisi|di mana|dimana|tolong|carikan|perpustakaan|it del)\b', '', query, flags=re.IGNORECASE).strip()
        search_query = clean_q if len(clean_q) >= 3 else query

        # Cari menggunakan hybrid search terfilter dahulu
        results = self.recommendation.recommend_by_query(
            query=search_query,
            limit=3,
            filter_params=filter_params if filter_params else None
        )
            
        # Fallback menggunakan pencarian klasifikasi murni jika hasil kosong
        if not results and class_num:
            results = self.retrieval.search_by_classification(class_num, limit=3)
            
        return results

    def del_website_search_tool(self, query: str) -> Optional[str]:
        """
        Melakukan pencarian dinamis di situs IT Del (https://www.del.ac.id/).
        Mendukung Google Custom Search API jika GOOGLE_API_KEY & GOOGLE_SEARCH_CX tersedia di env.
        Jika tidak tersedia, menggunakan RAG fallback lokal yang berisi informasi profil IT Del.
        """
        import os
        import requests
        
        api_key = os.getenv("GOOGLE_API_KEY")
        cx = os.getenv("GOOGLE_SEARCH_CX")
        
        # 1. Jika ada kredensial API Google, lakukan pencarian web riil
        if api_key and cx:
            try:
                print(f"[SEARCH TOOL] Querying Google Custom Search for: {query} (site:del.ac.id)")
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": api_key,
                    "cx": cx,
                    "q": f"{query} site:del.ac.id",
                    "num": 3
                }
                resp = requests.get(url, params=params, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    if items:
                        snippets = []
                        for i, item in enumerate(items):
                            snippets.append(f"[{i+1}] Source: {item.get('link')}\nContent: {item.get('snippet')}")
                        return "\n\n".join(snippets)
            except Exception as e:
                print(f"[SEARCH TOOL] Google API error: {e}, falling back to local database.")
                
        # 2. Fallback Lokal (Mock Scraper berisi profil IT Del)
        q_clean = query.lower().strip()
        
        # Database profil IT Del statis untuk simulasi
        mock_db = {
            "prodi": (
                "Institut Teknologi Del (IT Del) memiliki 10 Program Studi yang tersebar di 4 Fakultas:\n"
                "1. Fakultas Informatika dan Teknik Elektro (FITE):\n"
                "   - S1 Informatika\n"
                "   - S1 Sistem Informasi\n"
                "   - S1 Teknik Elektro\n"
                "2. Fakultas Teknologi Industri (FTI):\n"
                "   - S1 Manajemen Rekayasa\n"
                "   - S1 Teknik Metalurgi\n"
                "   - S1 Teknik Bioproses\n"
                "3. Fakultas Bioteknologi (FB):\n"
                "   - S1 Bioteknologi\n"
                "4. Fakultas Vokasi (FV):\n"
                "   - D4 Teknologi Rekayasa Perangkat Lunak (TRPL)\n"
                "   - D3 Teknologi Informasi (TI)\n"
                "   - D3 Teknologi Komputer (TK)"
            ),
            "rektor": "Rektor Institut Teknologi Del saat ini dijabat oleh Prof. Dr. Arnaldo Marulitua Sinaga, S.T., M.InfoTech.",
            "sejarah": (
                "Institut Teknologi Del didirikan pada tahun 2001 di Laguboti, Kabupaten Toba, Sumatera Utara. "
                "Didirikan oleh Bapak Luhut Binsar Pandjaitan di bawah naungan Yayasan Del untuk menyediakan pendidikan berkualitas tinggi."
            ),
            "visi": (
                "Visi Institut Teknologi Del: Menjadi pusat keunggulan yang berperan dalam pengembangan teknologi "
                "dan sumber daya manusia yang berdaya saing global, mandiri, dan berkarakter (MarTuhan, MarRoha, MarBisuk)."
            ),
            "biaya": (
                "Informasi biaya kuliah IT Del mencakup Biaya Penyelenggaraan Pendidikan (BPP/SPP) semester, uang pangkal, "
                "serta biaya asrama (boarding) karena seluruh mahasiswa wajib tinggal di asrama IT Del."
            ),
            "fasilitas": (
                "Fasilitas IT Del meliputi: Asrama mahasiswa, Kantin pusat, Gedung Perpustakaan, Laboratorium komputer/jaringan, "
                "Open Air Theater (OAT), Lapangan olahraga, Klinik kesehatan, dan lingkungan kampus hijau tepi Danau Toba."
            ),
            "pendaftaran": (
                "Penerimaan Mahasiswa Baru (PMB) IT Del dibuka melalui jalur USM (Ujian Penyaringan Masuk), PMDK (Jalur Prestasi), "
                "dan jalur nilai UTBK/SNBT. Informasi lengkap pendaftaran dapat diakses di pmb.del.ac.id."
            )
        }
        
        # Saringan pencocokan kata kunci
        keywords_map = {
            "prodi": ["prodi", "program studi", "jurusan", "fakultas", "fite", "fti"],
            "rektor": ["rektor", "pimpinan", "ketua", "arnaldo", "sinaga"],
            "sejarah": ["sejarah", "dirikan", "berdiri", "didirikan", "tahun berapa", "pendiri", "luhut", "yayasan del", "membangun", "mendirikan", "pembuat", "pembangunan"],
            "visi": ["visi", "misi", "semboyan", "martuhan", "marroha", "marbisuk"],
            "biaya": ["biaya", "uang sekolah", "spp", "bpp", "asrama", "bayar"],
            "fasilitas": ["fasilitas", "gedung", "asrama", "kantin", "lab", "klinik"],
            "pendaftaran": ["pendaftaran", "pmb", "masuk", "daftar", "usm", "pmdk"]
        }
        
        matched_contexts = []
        for key, kws in keywords_map.items():
            if any(kw in q_clean for kw in kws):
                matched_contexts.append(mock_db[key])
                
        if matched_contexts:
            return "\n\n".join(matched_contexts)
            
        return None
