from __future__ import annotations

from typing import Any, Dict, List


class BookChunker:
    """
    Membagi deskripsi buku menjadi chunk yang lebih kecil jika terlalu panjang.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_description(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []
        
        text = text.strip()
        if len(text) <= self.chunk_size:
            return [text]
            
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
            
        return chunks

    def chunk_book(self, book_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Membuat salinan payload buku untuk setiap chunk deskripsi.
        """
        description = book_payload.get("description", "") or book_payload.get("deskripsi", "")
        chunks = self.chunk_description(description)
        
        if not chunks:
            # Jika tidak ada deskripsi, return payload asli dengan deskripsi kosong
            return [book_payload]
            
        chunked_books = []
        for idx, chunk in enumerate(chunks):
            new_book = book_payload.copy()
            new_book["text"] = f"Judul: {book_payload.get('title', '')}\nDeskripsi: {chunk}"
            new_book["chunk_index"] = idx
            chunked_books.append(new_book)
            
        return chunked_books
