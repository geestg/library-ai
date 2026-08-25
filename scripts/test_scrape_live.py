#!/usr/bin/env python3
"""
Test Live Scraper untuk Repositori IT Del (ri.del.ac.id)
Mencoba mengunduh 1 skripsi live dan mengekstrak metadatanya.
"""

import urllib.request
import urllib.error
import re
from bs4 import BeautifulSoup

TARGET_URL = "http://ri.del.ac.id:8080/xmlui/handle/123456789/1285"
ALT_URL = "http://ri.del.ac.id/xmlui/handle/123456789/1285"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_scrape(url):
    print(f"\n[TEST SCRAPER] Menghubungi URL: {url}")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode("utf-8", errors="ignore")
            print(f"  [SUCCESS] Berhasil terhubung! (Ukuran HTML: {len(html)} bytes)")
            
            soup = BeautifulSoup(html, "html.parser")
            
            # Ekstrak Judul
            title = soup.find("h2", class_="page-header-heading") or soup.find("h1")
            title_text = title.get_text(strip=True) if title else "Tidak ditemukan"
            
            # Ekstrak Penulis
            author = soup.find("span", class_="author") or soup.find("div", class_="simple-item-view-author")
            author_text = author.get_text(strip=True) if author else "Tidak ditemukan"
            
            # Ekstrak Abstrak
            abstract = soup.find("div", class_="simple-item-view-description") or soup.find("div", class_="abstract")
            abstract_text = abstract.get_text(strip=True) if abstract else "Tidak ditemukan"
            
            # Ekstrak Link PDF
            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
            
            print(f"\n  [METADATA EXTRACTION RESULT]:")
            print(f"  - Judul    : {title_text}")
            print(f"  - Penulis  : {author_text}")
            print(f"  - Abstrak  : {abstract_text[:200]}...")
            print(f"  - File PDF : {pdf_links if pdf_links else 'Terkunci / Tidak ada link publik'}")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"  [HTTP ERROR] {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"  [CONNECTION FAILED]: {e.reason}")
        print(f"  (Catatan: Port 8080 repositori DSpace kampus IT Del biasanya hanya terbuka dari dalam jaringan LAN / VPN kampus).")
    except Exception as e:
        print(f"  [ERROR]: {e}")
    return False

if __name__ == "__main__":
    print("="*60)
    print("    UJI COBA SCRAPING LIVE REPOSITORI SKRIPSI IT DEL        ")
    print("="*60)
    
    success = test_scrape(TARGET_URL)
    if not success:
        test_scrape(ALT_URL)
