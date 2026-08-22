import re
from typing import Dict, Any, Optional

class LibraryParser:
    """
    Parser untuk mengekstrak entitas metadata (penulis, penerbit, nomor klasifikasi, letak lantai)
    dari kueri bahasa alami pengguna.
    """
    def __init__(self):
        # Triggers pattern dengan modifikasi [^,?\n]+ untuk inisial nama dengan titik (contoh: C.J. Date, J.K. Rowling)
        self.author_patterns = [
            re.compile(r"(?:ditulis oleh|karangan|karya|oleh|dari penulis)\s+([^,?\n]+)", re.IGNORECASE),
            re.compile(r"buku\s+([^,?\n]+)\s+(?:tentang|mengenai)", re.IGNORECASE)
        ]
        self.publisher_patterns = [
            re.compile(r"(?:terbitan|penerbit|dipublikasikan oleh)\s+([^,?\n]+)", re.IGNORECASE),
            re.compile(r"diterbitkan oleh\s+([^,?\n]+)", re.IGNORECASE)
        ]
        self.class_patterns = [
            re.compile(r"(?:klasifikasi|no\s+klasifikasi|kode|rak nomor|nomor|no)\s+(\d{3}(?:\.\d+)?)", re.IGNORECASE),
            re.compile(r"\b(\d{3}\.\d+)\b")
        ]
        self.location_patterns = [
            re.compile(r"\b(lt\s*\d+|lantai\s*\d+|lantai\s*(?:satu|dua|tiga|empat|lima|1|2|3|4|5))\b", re.IGNORECASE),
            re.compile(r"\b(rak\s*[a-zA-Z0-9/]+)\b", re.IGNORECASE)
        ]
        
        # Kamus konversi angka tekstual lantai ke format standard "Lt.X"
        self.floor_translation = {
            "satu": "1",
            "dua": "2"
        }

    def _clean_extracted_value(self, text: str) -> str:
        """
        Membersihkan kata sambung noise dan sisa preposisi di awal/akhir nilai terekstrak
        agar filter pencarian lebih bersih.
        """
        text = text.strip()
        
        # Bersihkan noise preposisi bahasa/tempat di awal teks
        noise_prefixes = [
            r"^di\s+", r"^pada\s+", r"^tentang\s+", r"^mengenai\s+",
            r"^karya\s+", r"^oleh\s+", r"^penerbit\s+", r"^terbitan\s+"
        ]
        for pattern in noise_prefixes:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
            
        # Bersihkan noise di akhir teks (misal: "di lt 1", "karya ...")
        noise_suffixes = [
            r"\s+di\s+lt\s*\d+$", r"\s+di\s+lantai\s*\d+$",
            r"\s+karya\s+.*$", r"\s+oleh\s+.*$", r"\s+terbitan\s+.*$"
        ]
        for pattern in noise_suffixes:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
            
        return text

    def _extract_location(self, text: str) -> Optional[str]:
        """
        Mengekstrak letak lantai fisik (Lt.1, Lt.2) dari teks kueri.
        Mendukung konversi angka tekstual ("lantai satu" -> "Lt.1").
        """
        for pattern in self.location_patterns:
            match = pattern.search(text)
            if match:
                loc_str = match.group(1).lower().strip()
                
                # Konversi angka tekstual jika ada
                for text_num, digit in self.floor_translation.items():
                    if text_num in loc_str:
                        loc_str = loc_str.replace(text_num, digit)
                        
                # Ambil digit angka lantai
                digit_match = re.search(r"\d+", loc_str)
                if digit_match:
                    return f"Lt.{digit_match.group(0)}"
                
                # Fallback jika hanya rak yang ditemukan
                if "rak" in loc_str:
                    return match.group(1).strip()
        return None

    def _extract_author(self, text: str) -> Optional[str]:
        for pattern in self.author_patterns:
            match = pattern.search(text)
            if match:
                val = self._clean_extracted_value(match.group(1))
                if val:
                    return val
        return None

    def _extract_publisher(self, text: str) -> Optional[str]:
        for pattern in self.publisher_patterns:
            match = pattern.search(text)
            if match:
                val = self._clean_extracted_value(match.group(1))
                if val:
                    return val
        return None

    def _extract_classification_number(self, text: str) -> Optional[str]:
        for pattern in self.class_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return None

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Mengekstrak seluruh filter metadata dari kueri.
        """
        return {
            "location": self._extract_location(query),
            "language": None,
            "subject": None,
            "author": self._extract_author(query),
            "publisher": self._extract_publisher(query),
            "classification_number": self._extract_classification_number(query),
        }
