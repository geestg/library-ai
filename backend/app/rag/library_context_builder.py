from typing import List, Dict

def build_library_book_context(results: List[Dict]) -> str:
    """
    Build grounded context dengan Match Classification & Confidence Threshold:
    - Score >= 80% -> EXACT MATCH (Hasil Utama)
    - 55% <= Score < 80% -> RELATED BOOK (Koleksi Terkait)
    - Score < 55% -> REJECT (Dibuang / Tidak Ditampilkan)
    """
    if not results:
        return "STATUS: TIDAK ADA BUKU YANG DITEMUKAN."

    exact_matches = []
    related_books = []

    for result in results:
        payload = result.get("payload", {})
        title = payload.get("title", payload.get("judul", "Unknown Title"))
        author = payload.get("author", payload.get("penulis", "-"))
        subject = payload.get("subject", payload.get("subjek", "-"))
        location = payload.get("location", payload.get("lokasi", "-"))
        publisher = payload.get("publisher", payload.get("penerbit", "-"))
        year = payload.get("year", payload.get("tahun", "-"))
        isbn = payload.get("isbn", "-")
        description = payload.get("description", payload.get("deskripsi", ""))
        
        raw_score = result.get("rerank_score", result.get("score", 0))
        
        # Penilaian relevansi terukur & realistis
        if raw_score >= 1.5:
            percentage = min(98, int(85 + (raw_score - 1.5) * 4))
            match_type = "EXACT MATCH"
        elif raw_score >= -0.8:
            percentage = int(68 + (raw_score + 0.8) * 7)
            match_type = "RELATED BOOK"
        elif raw_score >= -2.0:
            percentage = int(54 + (raw_score + 2.0) * 11)
            match_type = "RELATED BOOK"
        else:
            # Score < -2.0 -> REJECT TOTAL (Mencegah buku tidak relevan seperti Data & Informasi IT Del)
            continue

        item_str = (
            f"📖 {title}\n"
            f"• Penulis: {author}\n"
            f"• Lokasi Rak: {location} | Klasifikasi: {subject}\n"
            f"• Tingkat Relevansi: {percentage}% [{match_type}]\n"
            f"• Ringkasan: {description[:300] if description else '-'}\n"
        )

        if percentage >= 80:
            exact_matches.append(item_str)
        else:
            related_books.append(item_str)

    output = []
    if exact_matches:
        output.append("=== DOKUMEN EXACT MATCH (HASIL UTAMA SANGAT RELEVAN) ===")
        output.extend(exact_matches)

    if related_books:
        output.append("=== KOLEKSI TERKAIT (RELATED BOOKS) ===")
        output.extend(related_books)

    if not exact_matches and not related_books:
        return "STATUS: RELEVANSI RENDAH (TIDAK ADA BUKU YANG MEMENUHI THRESHOLD RELEVANSI DI KATALOG)."

    return "\n\n".join(output)
