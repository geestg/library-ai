from __future__ import annotations

import re
from typing import List, Dict, Any


def normalize_book(doc: dict) -> dict:
    """
    Menormalisasi payload buku agar memiliki struktur seragam.
    """
    payload = doc.get("payload", doc)
    title = payload.get("title", "")
    author = payload.get("author", payload.get("penulis", "Unknown"))
    subject = payload.get("subject", payload.get("subjek", ""))
    publisher = payload.get("publisher", payload.get("penerbit", "Unknown"))
    class_no = str(payload.get("classification_number", "")).strip()
    isbn = payload.get("isbn", "")
    
    loc = payload.get("location", payload.get("lokasi", "")).strip()
    
    if not loc or loc == "-" or loc.lower() == "none":
        if class_no:
            match = re.match(r'^(\d+)', class_no)
            if match:
                class_val = int(match.group(1))
                if 1 <= class_val <= 600:
                    loc = "Lantai 1"
                elif 600 < class_val <= 999:
                    loc = "Lantai 2"
                else:
                    loc = "Lantai 2 Gedung Baru"
            else:
                loc = "Lantai 1"
        else:
            loc = "Lantai 1"
    else:
        if "lt" in loc.lower() or "lantai" in loc.lower():
            loc = loc.replace("Lt. ", "Lantai ").replace("Lt.", "Lantai ").replace("lt.", "Lantai ")
        else:
            loc = f"Lantai {loc}"
            
    return {
        "title": title,
        "author": author,
        "subject": subject,
        "publisher": publisher,
        "location": loc,
        "classification_number": class_no,
        "isbn": isbn,
    }


def deduplicate_books(books: List[dict]) -> List[dict]:
    """
    Mendeduplikasi daftar buku berdasarkan nama utama judul.
    """
    seen = set()
    unique = []
    for b in books:
        raw_title = b["title"].lower()
        main_title = re.split(r'[:\(]', raw_title)[0].strip()
        clean_title = re.sub(r'[^a-z0-9]', '', main_title)
        
        if clean_title and clean_title not in seen:
            seen.add(clean_title)
            unique.append(b)
    return unique


def build_sources(books: List[dict]) -> List[dict]:
    """
    Membangun daftar sumber terstruktur dari daftar buku.
    """
    sources = []
    for b in books:
        sources.append({
            "title": b.get("title", ""),
            "author": b.get("author", ""),
            "publisher": b.get("publisher", ""),
            "subject": b.get("subject", ""),
            "location": b.get("location", ""),
            "classification_number": b.get("classification_number", ""),
            "isbn": b.get("isbn", "")
        })
    return sources
