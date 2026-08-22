from __future__ import annotations

import re
from typing import Dict, List, Any

from app.core.config import settings
from app.services.llm.model_gateway import gateway
from app.services.library.academic.book_formatter import (
    normalize_book, deduplicate_books, build_sources
)


class AcademicIntentHandlers:
    """
    Kumpulan penangan intent (FAQ, Lokasi Rak, Metadata, & Rekomendasi RAG)
    untuk agen mahasiswa perpustakaan IT Del.
    """

    def __init__(self, tools):
        self.tools = tools

    def handle_faq(self, query: str, current_time: str = None, user_role: str = "student", history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Mengurusi kueri FAQ menggunakan FAQTool, dengan LLM fallback jika tidak ada kecocokan di database statis.
        """
        CONTINUATION_WORDS = ["boleh", "lanjut", "ya", "iya", "ok", "oke", "siap", "mau", "tentu", "minta", "tolong", "bisa", "mana", "tampilkan", "arahkan"]
        query_lower = query.strip().lower()
        is_continuation = query_lower in CONTINUATION_WORDS or (len(query_lower.split()) <= 2 and any(cw in query_lower for cw in CONTINUATION_WORDS))

        answer = None
        if not is_continuation:
            answer = self.tools.faq_tool(query)
        
        if answer and not is_continuation:
            # Jika FAQ match ditemukan, kembalikan jawaban langsung agar respons tetap ringkas.
            sources_list = [{"title": "SOP / Regulasi / FAQ Perpustakaan IT Del", "content": answer.strip()}]
            return {
                "intent": "faq",
                "response": answer.strip(),
                "sources": sources_list,
                "citations": sources_list,
            }

        # Cek jika ada informasi tambahan di website resmi IT Del
        web_context = ""
        if hasattr(self.tools, "del_website_search_tool"):
            search_q = query
            if is_continuation and history:
                # Ambil kueri pengguna sebelumnya dari riwayat
                for h in reversed(history):
                    if h.get("role") == "user":
                        search_q = f"{h.get('content')} {query}"
                        break
            web_context = self.tools.del_website_search_tool(search_q) or ""
            if web_context:
                web_context = f"\nInformasi Resmi Website IT Del:\n{web_context}\n"

        time_context = f"\nKonteks Waktu Saat Ini: {current_time}\n" if current_time else ""
        
        history_context = ""
        if history:
            formatted_turns = []
            for msg in history[-4:]:
                r_label = "Pengguna" if msg.get("role") == "user" else "DELBot"
                formatted_turns.append(f"{r_label}: {msg.get('content')}")
            history_context = "\nRiwayat Percakapan Sebelumnya:\n" + "\n".join(formatted_turns) + "\n"

        guest_instruction = ""
        if user_role.lower() == "guest":
            guest_instruction = (
                "PERINGATAN HAK AKSES TAMU (GUEST ROLE):\n"
                "• Pengguna saat ini adalah TAMU UMUM (GUEST).\n"
                "• Jawab HANYA pertanyaan seputar informasi umum kampus IT Del, lokasi, jam operasional, atau FAQ perpustakaan.\n"
                "• DILARANG keras menyusun draf bab skripsi, memberikan analisis ide penelitian mendalam, atau memberikan laporan sirkulasi internal perpustakaan.\n"
                "• Jika pengguna meminta fitur skripsi/riset/admin tersebut, TOLAK secara sopan dan minta pengguna untuk login menggunakan akun CIS IT Del.\n"
            )

        prompt = (
            "System: Anda adalah DELBot, asisten AI Perpustakaan Institut Teknologi Del. Sampaikan seluruh tanggapan HANYA dalam Bahasa Indonesia. DILARANG keras menulis aksara Mandarin.\n"
            f"{time_context}\n"
            f"{guest_instruction}\n"
            f"{history_context}\n"
            f"{web_context}\n"
            "Tugas Anda:\n"
            "1. Jawablah pertanyaan pengguna dengan memperhatikan Riwayat Percakapan Sebelumnya (jika pengguna merespon persetujuan seperti 'BOLEH', lanjutkan topik sebelumnya!).\n"
            "2. Jika ada informasi resmi website IT Del di atas, gunakan data tersebut untuk memberikan jawaban yang akurat mengenai kampus IT Del.\n"
            "3. Jika pengguna memperkenalkan diri (seperti 'nama saya dora'), sapalah mereka kembali dengan ramah.\n"
            "4. Jika pengguna bertanya tentang perihal perpustakaan Del di luar FAQ statis, berikan informasi jika Anda mengetahuinya secara umum.\n"
            "5. Usahakan tanggapan Anda singkat, interaktif, dan tidak kaku.\n\n"
            f"Input Pengguna Terbaru: {query}\n\n"
            "Jawaban DELBot:"
        )
        try:
            answer = gateway.generate_response(
                prompt=prompt,
                model=settings.DEFAULT_LLM,
                max_tokens=150
            )
            if not answer:
                raise ValueError("LLM returned empty/None response")
        except Exception as e:
            print(f"[LIBRARY FAQ LLM FALLBACK ERROR] {e}")
            answer = "Halo! Ada yang bisa saya bantu terkait informasi perpustakaan hari ini?"
            time_context = f"\nKonteks Waktu Saat Ini: {current_time}\n" if current_time else ""
            prompt = (
                "System: Anda adalah DELBot, asisten AI Perpustakaan Institut Teknologi Del. Sampaikan seluruh tanggapan HANYA dalam Bahasa Indonesia. DILARANG keras menulis aksara Mandarin.\n"
                f"{time_context}\n"
                f"{web_context}\n"
                "Tugas Anda:\n"
                "1. Jawablah pertanyaan atau sapaan pengguna secara ramah, santun, dan natural.\n"
                "2. Jika ada informasi resmi website IT Del di atas, gunakan data tersebut untuk memberikan jawaban yang akurat mengenai kampus IT Del.\n"
                "3. Jika pengguna memperkenalkan diri (seperti 'nama saya dora'), sapalah mereka kembali dengan ramah.\n"
                "4. Jika pengguna bertanya tentang perihal perpustakaan Del di luar FAQ statis, berikan informasi jika Anda mengetahuinya secara umum. Jika benar-benar tidak tahu, sarankan secara sopan untuk bertanya langsung kepada petugas perpustakaan di lokasi.\n"
                "5. Usahakan tanggapan Anda singkat, interaktif, dan tidak kaku.\n\n"
                f"Input Pengguna: {query}\n\n"
                "Jawaban DELBot:"
            )
            try:
                answer = gateway.generate_response(
                    prompt=prompt,
                    model=settings.DEFAULT_LLM,
                    max_tokens=150
                )
                if not answer:
                    raise ValueError("LLM returned empty/None response")
            except Exception as e:
                print(f"[LIBRARY FAQ LLM FALLBACK ERROR] {e}")
                answer = "Halo! Ada yang bisa saya bantu terkait informasi perpustakaan hari ini?"

        faq_sources = []
        if web_context:
            faq_sources.append({"title": "Website Resmi IT Del / Informasi PMB", "content": web_context.strip()})
        else:
            faq_sources.append({"title": "Basis Pengetahuan Umum IT Del", "content": answer.strip()})

        return {
            "intent": "faq",
            "response": answer,
            "sources": faq_sources,
            "citations": faq_sources,
        }

    def handle_status_or_location(self, query: str, metadata_filter: dict) -> Dict[str, Any]:
        """
        Mengurusi kueri letak rak fisik buku dengan memanggil physical_location_tool.
        """
        results = self.tools.physical_location_tool(query, metadata_filter)

        if not results:
            class_num = metadata_filter.get("classification_number")
            fallback_hint = ""
            if class_num:
                try:
                    match = re.match(r'^(\d+)', str(class_num))
                    if match:
                        num = int(match.group(1))
                        if num <= 600:
                            fallback_hint = f" Namun sebagai panduan umum, klasifikasi awalan {num} biasanya berada di Lantai 1."
                        elif num <= 999:
                            fallback_hint = f" Namun sebagai panduan umum, klasifikasi awalan {num} biasanya berada di Lantai 2."
                except Exception:
                    pass

            return {
                "intent": "status",
                "response": (
                    "Maaf, saya tidak menemukan informasi lokasi rak "
                    f"spesifik untuk buku tersebut di katalog perpustakaan IT Del.{fallback_hint}"
                ),
                "sources": [],
                "citations": []
            }

        normalized = [normalize_book(r) for r in results]
        unique_books = deduplicate_books(normalized)

        response_lines = ["Berikut adalah informasi lokasi rak buku:\n"]
        for idx, book in enumerate(unique_books[:3], start=1):
            title = book.get("title", "")
            author = book.get("author", "Unknown")
            loc = book.get("location", "Lt.1")
            class_no = book.get("classification_number")
            
            line = f"{idx}. 📖 **{title}**"
            if author and author != "Unknown":
                line += f" oleh *{author}*"
            line += f"\n   • 📍 **Lokasi Rak:** {loc}"
            if class_no:
                line += f"\n   • 🏷️ **Nomor Klasifikasi:** `{class_no}`"
            response_lines.append(line)

        response = "\n".join(response_lines)

        sources_list = build_sources(unique_books)
        return {
            "intent": "status",
            "response": response,
            "sources": sources_list,
            "citations": sources_list
        }

    def handle_recommendation(self, query: str, metadata_filter: dict, history: List[Dict[str, str]] = None, faq_context: str = "") -> Dict[str, Any]:
        """
        Mengurusi pencarian dan rekomendasi RAG dengan catalog_search_tool, lalu disintesis oleh LLM.
        """
        formatted_history = ""
        if history:
            for msg in history[-5:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                formatted_history += f"{role}: {msg['content']}\n"

        normalized = query.lower().strip()
        generic_keywords = {"buku", "carikan", "cari", "rekomendasi", "rekomendasikan", "mau", "ingin", "baca", "bacaan", "referensi", "dong", "tolong", "apa", "saja", "yang", "bagus", "menarik", "hanya", "itu", "kok", "dikit", "sedikit"}
        
        words = re.findall(r'\b\w+\b', normalized)
        followup_guide_keywords = [
            "panduan", "langkah", "rencana", "jadwal", "tahap", "tahapan", 
            "cara", "jelaskan", "contoh", "silabus", "materi", "bagaimana", 
            "buatkan", "kurikulum", "roadmap", "rangkuman", "kesimpulan"
        ]
        is_followup_guidance = any(kw in normalized for kw in followup_guide_keywords)
        
        if is_followup_guidance and history:
            prompt_chat = (
                "System: Anda adalah DELBot, AI Assistant Perpustakaan IT Del yang cerdas, ramah, dan suportif.\n"
                "Tugas Anda: Lanjutkan percakapan dengan pengguna secara natural dan terstruktur (seperti ChatGPT) berdasarkan Konteks Chat Sebelumnya.\n"
                "Instruksi:\n"
                "1. Jawablah permintaan pengguna (seperti panduan belajar, tahapan, penjelasan, atau materi) secara terstruktur, inspiratif, dan praktis.\n"
                "2. Hubungkan panduan Anda dengan buku-buku yang telah direkomendasikan sebelumnya di Konteks Chat jika relevan.\n"
                "3. DILARANG KERAS mencetak daftar rekomendasi buku baru lagi kecuali pengguna secara eksplisit memintanya!\n"
                "4. Gunakan format Markdown yang rapi (poin, langkah 1, langkah 2, dll).\n\n"
                f"Konteks Chat Sebelumnya:\n{formatted_history}\n"
                f"Permintaan Pengguna: {query}\n\n"
                "Jawaban Panduan DELBot:"
            )
            try:
                resp = gateway.generate_response(prompt=prompt_chat, model=settings.DEFAULT_LLM, max_tokens=1200)
                if resp:
                    return {"intent": "recommendation", "response": resp.strip(), "sources": [], "citations": []}
            except Exception as e:
                print(f"[CONVERSATIONAL FOLLOWUP ERROR] {e}")

        meaningful_words = [w for w in words if w not in generic_keywords]
        
        if len(meaningful_words) == 0 and not any(metadata_filter.values()):
            if history:
                prompt_chat = (
                    "System: Anda adalah DELBot, asisten AI Perpustakaan IT Del yang cerdas.\n"
                    "Tugas Anda: Lanjutkan percakapan dengan pengguna secara natural dan ramah berdasarkan konteks histori chat.\n"
                    f"Konteks Chat Sebelumnya:\n{formatted_history}\n"
                    f"Pengguna: {query}\n\n"
                    "Balasan DELBot:"
                )
                try:
                    resp = gateway.generate_response(prompt=prompt_chat, model=settings.DEFAULT_LLM, max_tokens=150)
                    return {"intent": "recommendation", "response": resp, "sources": [], "citations": []}
                except:
                    pass

            return {
                "intent": "recommendation",
                "response": "Boleh saya tahu buku di bidang apa yang Anda cari? (Misal: Pemrograman, Fisika, Bisnis)",
                "sources": [],
                "citations": []
            }

        more_books_patterns = [
            r"ada\s+(?:yang\s+)?lain",
            r"buku\s+(?:yang\s+)?lain",
            r"rekomendasi\s+(?:yang\s+)?lain",
            r"koleksi\s+(?:yang\s+)?lain",
            r"ada\s+lagi",
            r"masih\s+ada",
            r"selain\s+ini",
            r"hanya\s+\d+",
            r"hanya\s+ini",
            r"hanya\s+tiga",
            r"tampilkan\s+lagi",
            r"tampilkan\s+lainnya",
            r"yang\s+lain",
            r"more\s+books",
            r"other\s+books",
            r"any\s+other",
            r"lainnya",
        ]
        q_lower = query.lower()
        is_asking_more = any(re.search(pat, q_lower) for pat in more_books_patterns)
        
        search_query_term = query
        if is_asking_more and history:
            for msg in reversed(history):
                if msg.get("role") == "user":
                    user_msg = msg.get("content", "")
                    if not any(re.search(pat, user_msg.lower()) for pat in more_books_patterns):
                        search_query_term = user_msg
                        print(f"[FOLLOW-UP MORE BOOKS] Retained search topic from history: '{search_query_term}'")
                        break

        raw_results = self.tools.catalog_search_tool(search_query_term, metadata_filter, limit=30)

        results = []
        if raw_results:
            past_assistant_texts = [msg["content"].lower() for msg in history if msg["role"] == "assistant"] if history else []
            
            for r in raw_results:
                payload = r.get("payload", r)
                title_lower = str(payload.get("title", payload.get("judul", ""))).lower().strip()
                title_clean = re.sub(r'[^a-z0-9]', '', title_lower)
                
                already_recommended = False
                for past_text in past_assistant_texts:
                    past_clean = re.sub(r'[^a-z0-9]', '', past_text)
                    if title_clean and title_clean in past_clean:
                        already_recommended = True
                        break
                    main_title = re.split(r'[:\(]', title_lower)[0].strip()
                    main_clean = re.sub(r'[^a-z0-9]', '', main_title)
                    if len(main_clean) > 8 and main_clean in past_clean:
                        already_recommended = True
                        break
                
                if not already_recommended:
                    results.append(r)
            
            if not results:
                print("[FOLLOW-UP MORE BOOKS] All books for this topic have already been shown to user.")
            else:
                results = results[:5]

        if not results:
            prompt = (
                "System: Anda adalah DELBot, asisten AI Perpustakaan IT Del. Sampaikan seluruh tanggapan HANYA dalam Bahasa Indonesia.\n\n"
                f"Konteks Chat Sebelumnya:\n{formatted_history}\n"
                f"Pengguna mencari rekomendasi buku untuk topik: '{query}' dengan filter: {metadata_filter}.\n\n"
                "Instruksi:\n"
                "1. Jika kueri adalah obrolan lanjutan (misal 'hanya itu?'), balaslah secara natural sesuai histori chat.\n"
                "2. Jika kueri adalah permintaan buku spesifik, sampaikan secara sopan bahwa saat ini koleksi perpustakaan tidak memiliki buku yang cocok. Sarankan 3 kata kunci alternatif yang lebih umum.\n"
                "PENTING: Jangan merekomendasikan judul buku spesifik fiktif."
            )
            try:
                fallback_resp = gateway.generate_response(
                    prompt=prompt,
                    model=settings.DEFAULT_LLM,
                    max_tokens=150
                )
                return {
                    "intent": "recommendation",
                    "response": fallback_resp,
                    "sources": [],
                    "citations": []
                }
            except Exception as e:
                print(f"[LIBRARY RECOMMENDATION LLM FALLBACK ERROR] {e}")
                return {
                    "intent": "recommendation",
                    "response": (
                        "Maaf, saya tidak menemukan buku yang cocok untuk rekomendasi tersebut di katalog saat ini. "
                        "Silakan coba dengan topik atau kata kunci lain."
                    ),
                    "sources": [],
                    "citations": []
                }

        normalized = [normalize_book(r) for r in results]
        unique_books = deduplicate_books(normalized)[:5]

        books_context = ""
        for idx, book in enumerate(unique_books, start=1):
            books_context += (
                f"{idx}. Judul: {book['title']}\n"
                f"   Penulis: {book['author']}\n"
                f"   Penerbit: {book['publisher']}\n"
                f"   Lokasi Rak: {book['location']}\n"
                f"   No Klasifikasi: {book['classification_number']}\n\n"
            )

        faq_block = f"Fakta FAQ Perpustakaan:\n{faq_context}\n" if faq_context and faq_context.strip() else ""
        faq_rule = "1. JAWAB FAQ TERLEBIH DAHULU: Sampaikan fakta FAQ perpustakaan secara singkat di awal kalimat.\n" if faq_block else ""

        prompt = (
            "System: Anda adalah DELBot, AI Assistant Perpustakaan Institut Teknologi Del. Sampaikan seluruh tanggapan HANYA dalam Bahasa Indonesia.\n\n"
            "Tugas Anda: Anda adalah seorang Asisten Peneliti Akademik. Berikan rekomendasi buku kepada pengguna berdasarkan Konteks Buku yang telah dicari dari database perpustakaan.\n\n"
            "Aturan Penulisan Jawaban (SANGAT PENTING):\n"
            f"{faq_rule}"
            "2. BUKTI KATALOG: Setiap rekomendasi BUKAN opini Anda, melainkan fakta dari katalog perpustakaan.\n"
            "3. FORMAT SETIAP BUKU DI KONTEKS: Judul (📖), Penulis (• 👤), Lokasi Rak & Klasifikasi (• 📍), dan Ringkasan (• 📝). DILARANG KERAS MENCETAK HEADER 'Academic Reasoning' ATAU 'Catatan' TERPISAH!\n"
            "4. ANTI-HALUSINASI: Jika buku di Konteks kurang relevan, jelaskan dengan jujur pada poin Ringkasan mengapa buku tersebut adalah alternatif terbaik yang ada saat ini di perpustakaan.\n"
            "5. DILARANG KERAS MENGULANG TEKS CHAT SEBELUMNYA: Jangan pernah mengulang kalimat sapaan, ucapan denda, atau balasan dari Konteks Chat Sebelumnya di awal jawaban.\n"
            "6. Gunakan HANYA informasi dari Konteks Buku yang disediakan. Jangan mengarang penulis, penerbit, atau letak rak.\n"
            "7. FORMAT WAJIB PER BUKU:\n"
            "   📖 **[Judul Buku]**\n"
            "   • 👤 Penulis: [Nama Penulis]\n"
            "   • 📍 Lokasi Rak: [Lokasi] | Klasifikasi: [Nomor]\n"
            "   • 📝 Ringkasan: [Ulasan Ringkas & Alasan Akademik (Maksimal 2 kalimat)]\n"
            "8. PENTING: Dilarang keras menyelipkan karakter atau bahasa asing/Mandarin.\n\n"
            f"Konteks Chat Sebelumnya:\n{formatted_history}\n"
            f"{faq_block}"
            f"Konteks Buku Perpustakaan:\n{books_context}\n"
            f"Kebutuhan / Pertanyaan Pengguna Saat Ini: {query}\n\n"
            "Rekomendasi DELBot (Evidence Engine & Conversational):"
        )

        sources_list = build_sources(unique_books)
        try:
            response = gateway.generate_response(
                prompt=prompt,
                model=settings.DEFAULT_LLM,
                max_tokens=750
            )
            if not response:
                raise ValueError("LLM returned empty/None response")
            return {
                "intent": "recommendation",
                "response": response,
                "sources": sources_list,
                "citations": sources_list
            }
        except Exception as e:
            print(f"[LIBRARY RECOMMENDATION SYNTHESIS ERROR] {e}")
            fallback_lines = ["Berikut adalah rekomendasi buku yang saya temukan:\n"]
            for idx, b in enumerate(unique_books, start=1):
                fallback_lines.append(f"{idx}. 📖 **{b['title']}** oleh *{b['author']}* (Penerbit: {b['publisher']}, Rak: {b['location']})")
            return {
                "intent": "recommendation",
                "response": "\n".join(fallback_lines),
                "sources": sources_list,
                "citations": sources_list
            }
