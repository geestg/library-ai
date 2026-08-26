import os
import sys
import re
import io
import json
import time
import shutil
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from pypdf import PdfReader

BASE_URL = "http://172.21.99.6:8080"
HEADERS = {"Host": "ri.del.ac.id:8080", "User-Agent": "Mozilla/5.0"}
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "delbot_platform", "workflows", "dataset", "skripsi_dataset_enriched.json")
BACKUP_PATH = DATASET_PATH + ".bak_pre_local"

def clean_text(t: str) -> str:
    if not t:
        return ""
    t = str(t).encode("utf-8", "ignore").decode("utf-8", "ignore")
    t = re.sub(r"[\ud800-\udfff]", "", t)
    t = re.sub(r"\r\n", " ", t)
    t = re.sub(r"\n+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_pdf(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            reader = PdfReader(io.BytesIO(r.read()))
            pages = [p.extract_text() for p in reader.pages[:35] if p.extract_text()]
            return " ".join(pages)
    except Exception:
        return ""

def process_item(item: dict) -> tuple:
    url = item.get("url", "")
    if not url or "123456789" not in url:
        return item, False
    
    clean_url = url.replace("http://ri.del.ac.id:8080", BASE_URL).replace("http://ri.del.ac.id", BASE_URL)
    
    try:
        req = urllib.request.Request(clean_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return item, False

    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Title
    if not item.get("title"):
        title_tag = soup.find("h2", class_="page-header-heading") or soup.find("h1") or soup.find("h2")
        if title_tag:
            item["title"] = clean_text(title_tag.get_text())

    # 2. Author
    if not item.get("author") or item.get("author") == "Unknown":
        author_div = soup.find("span", class_="author") or soup.find("div", class_="simple-item-view-authors") or soup.find("div", class_="author")
        if author_div:
            item["author"] = clean_text(re.sub(r"^(author|authors|penulis|peneliti)\s*:\s*", "", author_div.get_text(), flags=re.I))

    # 3. Abstract
    current_abs = item.get("abstract", "") or ""
    if len(current_abs) < 20:
        abs_tag = soup.find("div", class_="simple-item-view-description") or soup.find("div", class_="abstract")
        if abs_tag:
            extracted_abs = clean_text(abs_tag.get_text())
            item["abstract"] = clean_text(re.sub(r"^(abstract|abstrak)\s*:\s*", "", extracted_abs, flags=re.I))

    # 4. Content chapters
    content = item.get("content") or {}
    if not isinstance(content, dict):
        content = {}
    
    b1_text = content.get("bab1", "") or ""
    b3_text = content.get("bab3", "") or ""
    b5_text = content.get("bab5", "") or ""
    
    bitstream_links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if "/bitstream/" in href:
            full_link = BASE_URL + href if href.startswith("/") else href
            unquoted = urllib.parse.unquote(href).lower()
            text_desc = clean_text(a.get_text()).lower()
            bitstream_links.append((full_link, unquoted, text_desc))

    # Try matching bitstreams
    for full_link, unquoted, text_desc in bitstream_links:
        combined = f"{unquoted} {text_desc}"
        
        # Bab 1
        if len(b1_text) < 30 and re.search(r"(bab[\s_-]*(?:1|i)\b|chapter[\s_-]*(?:1|i)\b|pendahuluan|01_bab|1\.\s*bab\s*1)", combined):
            if "daftar" not in combined and "cover" not in combined:
                extracted = extract_pdf(full_link)
                if len(extracted) > 30:
                    b1_text = clean_text(extracted)
                    
        # Bab 3
        if len(b3_text) < 30 and re.search(r"(bab[\s_-]*(?:3|iii)\b|chapter[\s_-]*(?:3|iii)\b|metodologi|metode|analisis|03_bab|3\.\s*bab\s*3)", combined):
            if "daftar" not in combined:
                extracted = extract_pdf(full_link)
                if len(extracted) > 30:
                    b3_text = clean_text(extracted)

        # Bab 5 / Kesimpulan
        if len(b5_text) < 30 and re.search(r"(bab[\s_-]*(?:5|v|6|vi|7|vii)\b|chapter[\s_-]*(?:5|v|6|vi|7|vii)\b|kesimpulan|penutup|conclusion|05_bab|5\.\s*bab\s*5)", combined):
            if "daftar" not in combined:
                extracted = extract_pdf(full_link)
                if len(extracted) > 30:
                    b5_text = clean_text(extracted)

        # Abstract fallback from PDF
        if len(item.get("abstract", "") or "") < 20 and re.search(r"(abstrak|abstract|ringkasan)", combined):
            extracted = extract_pdf(full_link)
            if len(extracted) > 20:
                item["abstract"] = clean_text(re.sub(r"^(abstract|abstrak)\s*:\s*", "", extracted, flags=re.I))

    # If Bab 1 / Bab 3 / Bab 5 still missing, check if there is a Fulltext PDF
    if (len(b1_text) < 30 or len(b3_text) < 30 or len(b5_text) < 30):
        for full_link, unquoted, text_desc in bitstream_links:
            combined = f"{unquoted} {text_desc}"
            if re.search(r"(fulltext|tugas\s*akhir|skripsi|ta_\d+)", combined):
                full_extracted = extract_pdf(full_link)
                if len(full_extracted) > 200:
                    if len(b1_text) < 30:
                        b1_text = clean_text(full_extracted[:3000])
                    if len(b5_text) < 30:
                        b5_text = clean_text(full_extracted[-3000:])
                break

    item["content"] = {
        "bab1": clean_text(b1_text),
        "bab3": clean_text(b3_text),
        "bab5": clean_text(b5_text)
    }
    
    is_updated = (len(b1_text) > 30 or len(b3_text) > 30 or len(b5_text) > 30 or len(item.get("abstract", "") or "") > 20)
    return item, is_updated

def main():
    print("=" * 70, flush=True)
    print("     DELBOT LOCAL REPOSITORY ENRICHER & THESIS SCRAPER        ", flush=True)
    print("=" * 70, flush=True)
    print(f"Target DSpace Internal IP : {BASE_URL}", flush=True)
    print(f"Dataset path              : {DATASET_PATH}", flush=True)
    
    if not os.path.exists(DATASET_PATH):
        print(f"Error: dataset not found at {DATASET_PATH}", flush=True)
        return
        
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Total records in dataset: {len(data)}", flush=True)
    
    # Filter incomplete items
    incomplete_indices = []
    for idx, item in enumerate(data):
        content = item.get("content") or {}
        b1 = len(content.get("bab1", "") or "")
        b3 = len(content.get("bab3", "") or "")
        b5 = len(content.get("bab5", "") or "")
        abst = len(item.get("abstract", "") or "")
        if b1 < 30 or b3 < 30 or b5 < 30 or abst < 20:
            incomplete_indices.append(idx)
            
    print(f"Records needing enrichment: {len(incomplete_indices)} / {len(data)}", flush=True)
    if not incomplete_indices:
        print("All records already have complete content!", flush=True)
        return

    enriched_count = 0
    start_time = time.time()
    
    def save_checkpoint():
        temp_file = DATASET_PATH + ".tmp"
        with open(temp_file, "w", encoding="utf-8", errors="ignore") as tf:
            json.dump(data, tf, indent=4, ensure_ascii=False)
        shutil.move(temp_file, DATASET_PATH)

    print("Starting multithreaded extraction (12 workers)...", flush=True)
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_idx = {
            executor.submit(process_item, data[idx]): idx 
            for idx in incomplete_indices
        }
        
        completed = 0
        total_to_process = len(incomplete_indices)
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            completed += 1
            try:
                updated_item, is_updated = future.result()
                data[idx] = updated_item
                if is_updated:
                    enriched_count += 1
                
                title_short = (data[idx].get("title", "") or "Untitled")[:45]
                if completed % 5 == 0 or completed == total_to_process:
                    elapsed = time.time() - start_time
                    rate = completed / max(1, elapsed)
                    percent = (completed / total_to_process) * 100
                    print(f"[{completed}/{total_to_process}] ({percent:.1f}%) [{rate:.1f} item/s] - Sukses: {enriched_count} | {title_short}...", flush=True)
                    
                if completed % 25 == 0:
                    save_checkpoint()
                    print(f"  [CHECKPOINT DISIMPAN] Progress: {completed}/{total_to_process}", flush=True)
            except Exception as e:
                print(f"Error processing index {idx}: {e}", flush=True)
                
    save_checkpoint()
    elapsed = time.time() - start_time
    print("=" * 70, flush=True)
    print(f"ENRICHMENT SELESAI dalam {elapsed:.1f} detik!", flush=True)
    print(f"Total diproses : {len(incomplete_indices)}", flush=True)
    print(f"Total berhasil diperkaya : {enriched_count}", flush=True)
    print(f"Dataset tersimpan di: {DATASET_PATH}", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
