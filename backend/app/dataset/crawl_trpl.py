import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import io

BASE_URL = "http://ri.del.ac.id:8080"
COLLECTION_URL = f"{BASE_URL}/xmlui/handle/123456789/65"
if os.name == "nt":
    OUTPUT_FILE = "d:\\DEL\\library-ai\\backend\\app\\dataset\\skripsi_dataset_trpl.json"
    ENRICHED_DATASET_FILE = "d:\\DEL\\library-ai\\backend\\app\\dataset\\skripsi_dataset_enriched.json"
else:
    OUTPUT_FILE = "/app/app/dataset/skripsi_dataset_trpl.json"
    ENRICHED_DATASET_FILE = "/app/app/dataset/skripsi_dataset_enriched.json"

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\r\n", " ", text)
    text = re.sub(r"\n+",  " ", text)
    text = re.sub(r"\s+",  " ", text)
    return text.strip()

def extract_pdf_text(pdf_url: str) -> str:
    """Download a PDF and extract its text using pypdf."""
    try:
        print(f"      Downloading PDF: {pdf_url}")
        r = requests.get(pdf_url, timeout=15)
        if r.status_code == 200:
            f = io.BytesIO(r.content)
            reader = PdfReader(f)
            text_pages = []
            # Ambil maksimal 40 halaman agar tidak OOM
            max_pages = min(40, len(reader.pages))
            for i in range(max_pages):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    text_pages.append(page_text)
            return " ".join(text_pages)
        else:
            print(f"      [WARN] Failed to download PDF (HTTP {r.status_code})")
    except Exception as e:
        print(f"      [WARN] Error extracting PDF text: {e}")
    return ""

def scrape_item(item_url: str) -> dict:
    """Scrape title, author, year, abstract, and download PDF contents for one thesis item."""
    print(f"    Scraping item: {item_url}")
    try:
        r = requests.get(item_url, timeout=15)
        if r.status_code != 200:
            return None
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 1. Title
        title_tag = soup.find("h2", class_="heading") or soup.find("h2") or soup.find("h1")
        title = clean_text(title_tag.text) if title_tag else ""
        
        # 2. Author
        author_div = soup.find("div", class_="simple-item-view-authors") or soup.find("div", class_="author")
        author = clean_text(author_div.text) if author_div else "Unknown"
        # Hilangkan prefix "Author:" atau "Penulis:"
        author = re.sub(r"^(author|authors|penulis|peneliti)\s*:\s*", "", author, flags=re.IGNORECASE)
        
        # 3. Year
        date_div = soup.find("div", class_="simple-item-view-date") or soup.find("div", class_="date")
        date_str = clean_text(date_div.text) if date_div else ""
        year_match = re.search(r"\b(20\d{2})\b", date_str)
        year = int(year_match.group(1)) if year_match else 2024
        
        # 4. Abstract
        abstract_div = soup.find("div", class_="simple-item-view-description") or soup.find("div", class_="abstract")
        abstract = clean_text(abstract_div.text) if abstract_div else ""
        # Hilangkan prefix "Abstract:" atau "Abstrak:"
        abstract = re.sub(r"^(abstract|abstrak)\s*:\s*", "", abstract, flags=re.IGNORECASE)
        
        # 5. Extract PDF links
        bab1_text = ""
        bab3_text = ""
        bab5_text = ""
        
        bitstreams = soup.find_all("a", href=re.compile(r"/bitstream/"))
        for bs in bitstreams:
            href = bs.get("href", "")
            full_pdf_url = BASE_URL + href
            
            # Bab 1
            if re.search(r"bab%20i\b|bab%201\b", href, re.IGNORECASE) or "bab i.pdf" in bs.text.lower() or "bab 1.pdf" in bs.text.lower():
                bab1_text = extract_pdf_text(full_pdf_url)
            # Bab 3
            elif re.search(r"bab%20iii\b|bab%203\b", href, re.IGNORECASE) or "bab iii.pdf" in bs.text.lower() or "bab 3.pdf" in bs.text.lower():
                bab3_text = extract_pdf_text(full_pdf_url)
            # Bab 5
            elif re.search(r"bab%20v\b|bab%205\b", href, re.IGNORECASE) or "bab v.pdf" in bs.text.lower() or "bab 5.pdf" in bs.text.lower():
                bab5_text = extract_pdf_text(full_pdf_url)
                
        return {
            "title": title,
            "author": author,
            "year": year,
            "prodi": "Sarjana Terapan Teknologi Rekayasa Perangkat Lunak",
            "url": item_url,
            "abstract": abstract,
            "content": {
                "bab1": clean_text(bab1_text),
                "bab3": clean_text(bab3_text),
                "bab5": clean_text(bab5_text)
            }
        }
    except Exception as e:
        print(f"    [ERROR] Failed to scrape item {item_url}: {e}")
    return None

def start_crawl():
    print("=== D4 TRPL THESIS METADATA CRAWLER START ===")
    
    offset = 0
    all_item_links = []
    
    # Step 1: Ambil semua link detail item D4 TRPL
    while True:
        url = f"{COLLECTION_URL}?offset={offset}"
        print(f"Fetching Collection Page (Offset {offset}): {url}")
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                print(f"[WARN] Collection page return HTTP {r.status_code}. Stopping collection retrieval.")
                break
                
            soup = BeautifulSoup(r.text, "html.parser")
            # Cari link href yang mengarah ke handle item (/xmlui/handle/123456789/[id])
            links = soup.find_all("a", href=re.compile(r"/handle/123456789/\d+$"))
            
            page_links = []
            for link in links:
                href = link.get("href")
                full_item_url = BASE_URL + href
                if full_item_url not in all_item_links and full_item_url not in page_links:
                    page_links.append(full_item_url)
                    
            if not page_links:
                print("No more item links found. Stopping page collection.")
                break
                
            all_item_links.extend(page_links)
            print(f"  Found {len(page_links)} item links on this page. Total collected: {len(all_item_links)}")
            
            # Paginasi kelipatan 20
            offset += 20
            
            # Batasi paginasi (misal max 3 halaman = 60 paper teratas agar tidak terlalu lama)
            if offset >= 60:
                print("Pagination limit reached (60 items limit). Continuing to scrape item details.")
                break
        except Exception as e:
            print(f"[ERROR] Failed to fetch collection page: {e}")
            break
            
    print(f"\nTotal detail links gathered: {len(all_item_links)}")
    
    # Step 2: Ambil metadata & PDF teks untuk setiap link
    scraped_theses = []
    for idx, link in enumerate(all_item_links, start=1):
        print(f"\n[{idx}/{len(all_item_links)}] Scraping...")
        res = scrape_item(link)
        if res and res.get("title"):
            scraped_theses.append(res)
            
    # Step 3: Simpan data TRPL baru ke skripsi_dataset_trpl.json
    print(f"\n[DONE] Successfully scraped {len(scraped_theses)} TRPL items.")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(scraped_theses, f, indent=4, ensure_ascii=False)
    print(f"Saved to {OUTPUT_FILE}")
    
    # Step 4: Gabungkan ke skripsi_dataset_enriched.json
    if os.path.exists(ENRICHED_DATASET_FILE):
        try:
            with open(ENRICHED_DATASET_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception as e:
            print(f"Failed to load existing enriched dataset: {e}")
            existing_data = []
    else:
        existing_data = []
        
    # Hindari duplikasi URL saat menggabungkan
    existing_urls = {item.get("url") for item in existing_data if item.get("url")}
    added_count = 0
    for new_item in scraped_theses:
        if new_item.get("url") not in existing_urls:
            existing_data.append(new_item)
            added_count += 1
            
    print(f"Merged {added_count} new TRPL items into {ENRICHED_DATASET_FILE} (Total records: {len(existing_data)})")
    
    with open(ENRICHED_DATASET_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
    print("Dataset merge completed successfully!")

if __name__ == "__main__":
    start_crawl()
