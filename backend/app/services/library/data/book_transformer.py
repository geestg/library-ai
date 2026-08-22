from __future__ import annotations

import re
from typing import Any, Dict
from app.services.library.data.book_chunker import BookChunker


def remove_empty_fields(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None and str(v).strip() != ""}

def clean_numeric_to_str(val: Any) -> str:
    """
    Membersihkan float dari Excel menjadi string bersih.
    Juga mengatasi masalah Scientific Notation pada ISBN besar (misal 9.78E+12).
    """
    if val is None:
        return ""
    if isinstance(val, str) and 'E' in val.upper():
        try:
            val = float(val)
        except ValueError:
            pass
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        return f"{val:.0f}"
    return str(val).strip()

def sanitize_text_for_hash(text: str) -> str:
    """
    Membersihkan teks dari tanda baca dan penyeragaman konjungsi agar hash identik (Anti ganda).
    """
    if not text:
        return ""
    text = str(text).lower()
    # Ganti ampersand dan "dan" menjadi "and" untuk seragam
    text = text.replace("&", " and ").replace(" dan ", " and ")
    # Hapus semua tanda baca
    text = re.sub(r'[^\w\s]', '', text)
    # Rapatkan spasi
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def sanitize_author(author: str) -> str:
    """
    Memperbaiki format penulis (misal: "Kadir. Abdul" -> "Kadir, Abdul")
    """
    if not author:
        return "Unknown"
    author = str(author).strip()
    # Ganti titik yang salah jadi koma jika format "Lastname. Firstname"
    author = re.sub(r'([A-Za-z]+)\.\s+([A-Za-z]+)', r'\1, \2', author)
    # Title Case
    return author.title()

def normalize_location(loc: str, class_no: str) -> str:
    """
    Memperbaiki format nama lokasi / lantai rak.
    """
    loc = str(loc).strip()
    if not loc or loc == "-" or loc.lower() == "none":
        if class_no:
            match = re.match(r'^(\d+)', class_no)
            if match:
                class_val = int(match.group(1))
                if 1 <= class_val <= 600:
                    return "Lantai 1"
                elif 600 < class_val <= 999:
                    return "Lantai 2"
                else:
                    return "Lantai 2 Gedung Baru"
        return "Lantai 1"
    
    if "lt" in loc.lower() or "lantai" in loc.lower():
        loc = loc.replace("Lt. ", "Lantai ").replace("Lt.", "Lantai ").replace("lt.", "Lantai ")
    else:
        loc = f"Lantai {loc}"
    return loc


class BookTransformer:
    """
    Transformasi data katalog buku dari Excel (Indonesian fields) ke schema Qdrant (English fields)
    dengan TYPE CASTING super ketat untuk mencegah Panic Qdrant 500.
    """
    def __init__(self):
        self.chunker = BookChunker()

    def normalize_fields(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Memetakan kolom Excel ke key Qdrant payload dengan pembersihan tipe data ekstrim (Force String).
        """
        class_no = str(item.get("Classification Number") or item.get("klasifikasi_no") or "").strip()
        loc_raw = str(item.get("Location") or item.get("lokasi") or "").strip()
        
        normalized = {
            "title": str(item.get("Title") or item.get("judul") or "").strip(),
            "description": str(item.get("Deskripsi") or item.get("deskripsi") or "").strip(),
            "author": sanitize_author(item.get("Author") or item.get("penulis")),
            "published_at": clean_numeric_to_str(item.get("Published At") or item.get("tahun_terbit")),
            "publisher": str(item.get("Publisher") or item.get("penerbit") or "Unknown").strip(),
            "language": str(item.get("Language") or item.get("bahasa") or "English").strip(),
            "subject": str(item.get("Subject") or item.get("subjek") or "").strip(),
            "classification_number": class_no,
            "location": normalize_location(loc_raw, class_no),
            "isbn": clean_numeric_to_str(item.get("ISBN Number") or item.get("isbn")),
        }
        
        # total_pages MUST be int
        try:
            normalized["total_pages"] = int(float(item.get("Total Pages") or 0))
        except (ValueError, TypeError):
            normalized["total_pages"] = 0
            
        return remove_empty_fields(normalized)

    def build_text_field(self, item: Dict[str, Any]) -> str:
        """
        Membuat teks gabungan deskriptif yang akan di-embed. 
        Mengandung Semantic Expansion otomatis.
        """
        title = item.get("title") or ""
        subject = item.get("subject") or ""
        description = item.get("description") or ""
        author = item.get("author") or ""
        publisher = item.get("publisher") or ""
        location = item.get("location") or ""
        classification_number = item.get("classification_number") or ""

        # Semantic Pre-Expansion
        expanded_keywords = ""
        lower_title_subj = f"{title.lower()} {subject.lower()}"
        if " ai " in f" {lower_title_subj} " or "artificial intelligence" in lower_title_subj:
            expanded_keywords += " (Artificial Intelligence / Kecerdasan Buatan)"
        if " ml " in f" {lower_title_subj} " or "machine learning" in lower_title_subj:
            expanded_keywords += " (Machine Learning / Pembelajaran Mesin)"

        parts = []
        if title:
            parts.append(f"Judul: {title}{expanded_keywords}".strip())
        if author and author != "Unknown":
            parts.append(f"Penulis: {author}")
        if subject:
            parts.append(f"Subjek: {subject}")
        if publisher and publisher != "Unknown":
            parts.append(f"Penerbit: {publisher}")
        if classification_number:
            parts.append(f"Nomor Klasifikasi: {classification_number}")
        if location:
            parts.append(f"Lokasi Rak: {location}")
        if description:
            parts.append(f"Deskripsi: {description}")

        return "\n".join(parts).strip()

    def transform_book(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        normalized = self.normalize_fields(raw_item)
        normalized["text"] = self.build_text_field(normalized)
        
        # Bawa sanitized hash key ke payload untuk UUID builder
        normalized["_hash_title"] = sanitize_text_for_hash(normalized.get("title", ""))
        normalized["_hash_author"] = sanitize_text_for_hash(normalized.get("author", ""))
        return normalized
