from __future__ import annotations

import re
import json
from typing import Dict, List, Any

from delbot_platform.core.config import settings
from delbot_platform.ai.llm.model_gateway import gateway
from delbot_platform.knowledge.librarian.tools import LibraryLibrarianTools
from delbot_platform.knowledge.library.faq import answer_faq
from delbot_platform.knowledge.library.tools import LibraryAcademicTools


class LibraryLibrarianAgent:
    """
    LibraryLibrarianAgent adalah agen otonom khusus untuk Staf/Pustakawan Perpustakaan IT Del.
    Agen ini menggunakan Semantic Routing berbasis LLM untuk memilih perkakas (tool)
    secara dinamis dan mengekstrak parameternya, serta memiliki sistem fallback rule-based yang tangguh.
    """

    def __init__(self):
        self.tools = LibraryLibrarianTools()
        self.academic_tools = LibraryAcademicTools()

    def run(self, query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        EntryPoint Utama untuk Admin Agent.
        Menganalisis kueri admin menggunakan LLM routing, memicu tool yang sesuai,
        dan menyintesis tanggapan ramah staf.
        """
        if history is None:
            history = []

        query_clean = query.lower().strip()

        # 0. Cek jika ada FAQ statis langsung (Jam buka, Denda, Kalender Akademik, Alamat, Pendiri)
        faq_direct = answer_faq(query_clean)
        if faq_direct:
            return {
                "intent": "faq",
                "response": faq_direct.strip(),
                "sources": [],
                "citations": [],
                "data": None
            }

        tool_output = None
        tool_name = "no_tool"
        args = {}

        # Format riwayat obrolan (chat history)
        history_str = ""
        if history:
            history_str = "Riwayat Obrolan Sebelumnya:\n"
            for msg in history[-5:]: # Ambil 5 pesan terakhir
                role_name = "Staf" if msg.get("role") == "user" else "DELBot"
                history_str += f"{role_name}: {msg.get('content')}\n"
            history_str += "\n"

        # 1. Pemicuan Tool berbasis Agen LLM (Semantic Routing)
        router_prompt = (
            "System: Anda adalah Router Perutean Tool Cerdas untuk DELBot Admin Co-Pilot.\n"
            "Tugas Anda adalah menganalisis kueri staf perpustakaan dan memutuskan perkakas (tool) mana yang harus dijalankan beserta argumennya.\n"
            "Gunakan riwayat obrolan sebelumnya di bawah untuk memahami konteks kueri baru jika kueri merujuk ke hal sebelumnya (kata tunjuk seperti 'itu', 'yang tadi', dll.).\n\n"
            f"{history_str}"
            "Perkakas yang tersedia:\n"
            "1. `query_circulation`: Menampilkan data sirkulasi peminjaman aktif & denda buku. Menerima argumen opsional 'member_query' (nama atau NIM anggota) untuk mencari riwayat peminjaman, telat pengembalian, atau denda anggota tertentu.\n"
            "2. `query_insights`: Menampilkan statistik tren sirkulasi & kategori populer buku.\n"
            "3. `generate_report`: Membuat file Excel sirkulasi peminjaman & denda buku. JANGAN gunakan untuk log/kunjungan pengunjung.\n"
            "4. `list_datasets`: Menampilkan daftar file katalog/log di folder data. JANGAN gunakan untuk mencari buku atau rekomendasi buku.\n"
            "5. `sync_collection`: Sinkronisasi katalog buku baru ke Qdrant. Membutuhkan argumen 'filename' (nama file yang disebutkan).\n"
            "6. `analyze_visitor_log`: Menganalisis berkas log pengunjung (kedatangan fisik ke perpustakaan) secara umum/agregat (statistik total, jam sibuk, prodi teraktif). Menerima argumen opsional 'month'. JANGAN gunakan jika mencari nama/NIM/Prodi tertentu secara spesifik.\n"
            "7. `search_visitor`: Mencari riwayat kedatangan fisik/kunjungan anggota perpustakaan secara spesifik (nama, NIM, atau program studi tertentu). Membutuhkan argumen 'member_query' (misal: 'Risky', '12S23010', atau 'S1 Informatika'). JANGAN gunakan untuk menanyakan peminjaman, keterlambatan pengembalian buku, atau denda (gunakan 'query_circulation').\n"
            "8. `update_loan_status`: Memperbarui status peminjaman buku (misal: 'Kembali', 'Dipinjam', 'Dipinjam (Terlambat)') dan menyesuaikan denda. Membutuhkan argumen 'loan_id' (ID peminjaman, misal: 'L002') dan 'status' (status baru, misal: 'Kembali'). Argumen opsional: 'denda' (nominal rupiah/angka, misal: 0 atau 5000).\n"
            "9. `no_tool`: Tidak memicu perkakas apapun (misal: sapaan umum, obrolan santai, terima kasih, atau kueri rekomendasi/pencarian buku mahasiswa).\n\n"
            "Format Output: Anda HANYA boleh mengeluarkan format JSON valid seperti berikut tanpa penjelasan tambahan atau tanda kutip markdown:\n"
            "{\n"
            "  \"tool\": \"nama_tool\",\n"
            "  \"args\": {\"nama_argumen\": \"nilai_argumen\"}\n"
            "}\n\n"
            f"Kueri Staf Perpustakaan Baru: \"{query}\"\n"
            "Output JSON:"
        )

        try:
            router_response = gateway.generate_response(
                prompt=router_prompt,
                model=settings.DEFAULT_LLM
            )
            # Bersihkan markdown code block jika ada
            clean_json = re.sub(r'```json|```', '', router_response).strip()
            decision = json.loads(clean_json)
            
            tool_name = decision.get("tool")
            args = decision.get("args", {})
            
            print(f"[ADMIN AGENT ROUTER] Memicu perkakas: {tool_name} dengan argumen: {args}")
            
            if tool_name == "query_circulation":
                tool_output = self.tools.query_circulation(member_query=args.get("member_query"))
            elif tool_name == "query_insights":
                tool_output = self.tools.query_insights()
            elif tool_name == "generate_report":
                tool_output = self.tools.generate_report()
            elif tool_name == "list_datasets":
                tool_output = self.tools.list_datasets()
            elif tool_name == "sync_collection":
                tool_output = self.tools.sync_collection(args.get("filename", "buku_baru.xlsx"))
            elif tool_name == "analyze_visitor_log":
                tool_output = self.tools.analyze_visitor_log(
                    filename=args.get("filename", "log_pengunjung_Genap_2026.xlsx"),
                    month=args.get("month")
                )
            elif tool_name == "search_visitor":
                tool_output = self.tools.search_visitor(args.get("member_query", ""))
            elif tool_name == "update_loan_status":
                tool_output = self.tools.update_loan_status(
                    loan_id=args.get("loan_id", "L001"),
                    status=args.get("status", "Kembali"),
                    denda=args.get("denda")
                )
            elif tool_name == "no_tool":
                tool_output = "Sapaan / Bantuan Operasional Staf"
                
        except Exception as e:
            print(f"[ADMIN AGENT WARNING] Gagal menggunakan semantic routing: {e}. Mengaktifkan fallback rule-based routing.")

        # Fallback ke keyword-based routing jika semantic routing gagal atau tool_output kosong
        if not tool_output:
            if any(kw in query_clean for kw in ["selesaikan", "kembalikan", "update status", "bayar denda", "set denda"]):
                loan_match = re.search(r'\b(tx_\d+|l\d+|\d+)\b', query_clean)
                loan_id = loan_match.group(1).upper() if loan_match else "TX_00005"
                status_val = "Kembali"
                if "hilang" in query_clean:
                    status_val = "Hilang"
                elif "dipinjam" in query_clean:
                    status_val = "Dipinjam"
                denda_match = re.search(r'\b(?:denda\s*)?(\d+)\b', query_clean)
                denda_val = int(denda_match.group(1)) if denda_match else None
                tool_output = self.tools.update_loan_status(loan_id, status_val, denda_val)
            elif any(kw in query_clean for kw in ["cari riwayat", "cari pengunjung", "riwayat kunjungan", "kunjungan nim", "kunjungan nama"]):
                search_query = query_clean
                for stopword in ["cari", "riwayat", "kunjungan", "pengunjung", "tolong", "tampilkan", "file", "log", "log_pengunjung_genap_2026.xlsx", "siapa"]:
                    search_query = search_query.replace(stopword, "")
                search_query = search_query.strip()
                tool_output = self.tools.search_visitor(search_query)
            elif any(kw in query_clean for kw in ["pengunjung", "visitor", "kunjungan"]):
                file_match = re.search(r'\b[\w\.-]+\.(csv|xlsx|xls)\b', query_clean)
                filename = file_match.group(0) if file_match else "log_pengunjung_Genap_2026.xlsx"
                
                # Cari bulan sederhana di fallback
                month_val = None
                for m_kw in ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"]:
                    if m_kw in query_clean:
                        month_val = m_kw
                        break
                if not month_val:
                    m_num = re.search(r'\bbulan\s*(\d+)\b', query_clean)
                    if m_num:
                        month_val = m_num.group(1)
                        
                tool_output = self.tools.analyze_visitor_log(filename, month=month_val)
            elif any(kw in query_clean for kw in ["dashboard", "insight", "analisis", "tren", "populer"]):
                tool_output = self.tools.query_insights()
            elif any(kw in query_clean for kw in ["pinjam", "sirkulasi", "denda", "siapa yang pinjam"]):
                tool_output = self.tools.query_circulation()
            elif any(kw in query_clean for kw in ["laporan", "excel", "pdf", "ekspor", "print"]):
                tool_output = self.tools.generate_report()
            elif any(kw in query_clean for kw in ["daftar file", "lihat file", "list file", "folder data", "file yang ada"]):
                tool_output = self.tools.list_datasets()
            elif any(kw in query_clean for kw in ["sinkron", "sync", "unggah", "excel baru", "buku baru", ".xlsx", ".csv"]):
                file_match = re.search(r'\b[\w\.-]+\.(csv|xlsx|xls)\b', query_clean)
                filename = file_match.group(0) if file_match else "buku_baru.xlsx"
                tool_output = self.tools.sync_collection(filename)
            else:
                tool_output = "Sapaan / Bantuan Operasional Staf"

        # Cek jika ada informasi tambahan di website resmi IT Del
        web_context = ""
        if hasattr(self.academic_tools, "del_website_search_tool"):
            web_context = self.academic_tools.del_website_search_tool(query_clean) or ""
            if web_context:
                web_context = f"\nInformasi Resmi Website IT Del:\n{web_context}\n"

        # 2. Sintesis Tanggapan Menggunakan LLM
        tool_data = None
        if isinstance(tool_output, dict):
            tool_data = tool_output.get("data")
            tool_output = tool_output.get("text", "")

        prompt = (
            "System: Anda adalah DELBot Admin Agent Co-Pilot, asisten AI khusus Staf dan Pengelola Perpustakaan IT Del. Sampaikan seluruh tanggapan HANYA dalam Bahasa Indonesia.\n"
            "Gunakan riwayat obrolan di bawah untuk menjaga kesinambungan percakapan apabila kueri baru merujuk ke topik atau pertanyaan sebelumnya.\n\n"
            f"{history_str}"
            f"{web_context}"
            "Tugas Anda:\n"
            "1. Jawablah kueri staf perpustakaan dengan sikap profesional, solutif, dan informatif.\n"
            "2. Gunakan hasil dari perkakas (Tool Output) atau Informasi Resmi Website IT Del di atas sebagai sumber utama informasi Anda.\n"
            "3. Jika kueri staf menanyakan informasi umum kampus/perpustakaan (seperti kalender akademik, biaya kuliah, rektor, lokasi), berikan jawaban yang jelas dan lengkap.\n"
            "4. Jika Tool Output menunjukkan tautan unduhan Excel atau tabel denda, jelaskan dengan jelas dan ramah.\n"
            "5. PENTING: Jika di dalam Tool Output terdapat tag/kode placeholder seperti [PIE_CHART] atau [BAR_CHART], Anda WAJIB menuliskan kode tersebut persis apa adanya (verbatim) pada posisi semula di tanggapan akhir Anda. Jangan menerjemahkan, mengubah, atau menghapus kode [PIE_CHART] atau [BAR_CHART] tersebut karena frontend membutuhkannya untuk menggambar grafik.\n\n"
            f"Hasil Kerja Perkakas (Tool Output):\n{tool_output}\n\n"
            f"Kueri Staf Perpustakaan Baru: {query}\n\n"
            "Tanggapan DELBot Admin Co-Pilot:"
        )

        try:
            response = gateway.generate_response(
                prompt=prompt,
                model=settings.DEFAULT_LLM
            )
            return {
                "intent": "admin_co_pilot",
                "response": response,
                "sources": [],
                "citations": [],
                "data": tool_data
            }
        except Exception as e:
            # Fallback jika LLM gagal merespon
            return {
                "intent": "admin_co_pilot",
                "response": (
                    f"Berikut adalah hasil pemrosesan permintaan Anda:\n\n{tool_output}\n\n"
                    "Mohon maaf, saat ini sintesis bahasa sedang sibuk, namun tugas administrasi Anda telah selesai diproses."
                ),
                "sources": [],
                "citations": [],
                "data": tool_data
            }
