from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

META = ROOT / "delbot_platform/repository_data/metadata"
PDF = ROOT / "delbot_platform/repository_data/pdf"

print("=" * 80)
print("LOAD CATALOG")
print("=" * 80)

catalog_file = META / "repository_catalog.json"

catalog = json.loads(catalog_file.read_text(encoding="utf-8"))

print("Catalog Entries :", len(catalog))

print()
print("=" * 80)
print("LOAD PDF DIRECTORY")
print("=" * 80)

pdf_files = list(PDF.glob("*.pdf"))

pdf_ids = {p.stem for p in pdf_files}

print("PDF Files :", len(pdf_files))

print()
print("=" * 80)
print("CATALOG FIELD ANALYSIS")
print("=" * 80)

sample = catalog[0]

for k in sample.keys():
    print(k)

print()
print("=" * 80)
print("FIRST 20 CATALOG IDS")
print("=" * 80)

for item in catalog[:20]:
    print(item.get("document_id"))

print()
print("=" * 80)
print("FIRST 20 PDF IDS")
print("=" * 80)

for name in sorted(pdf_ids)[:20]:
    print(name)

print()
print("=" * 80)
print("DIRECT MATCH")
print("=" * 80)

matched = 0

for item in catalog:
    doc = item.get("document_id")
    if doc in pdf_ids:
        matched += 1

print("Matched :", matched)

print()
print("=" * 80)
print("MATCH USING pdf_path")
print("=" * 80)

matched_pdf_path = 0

for item in catalog:
    pdf_path = item.get("pdf_path")
    if not pdf_path:
        continue

    stem = Path(pdf_path).stem

    if stem in pdf_ids:
        matched_pdf_path += 1

print("Matched :", matched_pdf_path)

print()
print("=" * 80)
print("SEARCH UUID INSIDE RECORD")
print("=" * 80)

uuid_keys = []

for key in sample.keys():
    value = sample.get(key)

    if isinstance(value, str):

        if len(value) == 32:
            uuid_keys.append(key)

print("Possible UUID Keys :", uuid_keys)

for key in uuid_keys:
    print()
    print("KEY:", key)

    ok = 0

    for item in catalog:

        value = item.get(key)

        if value in pdf_ids:
            ok += 1

    print("Matched:", ok)

print()
print("=" * 80)
print("SEARCH ALL STRING VALUES")
print("=" * 80)

best_key = None
best_match = -1

keys = list(sample.keys())

for key in keys:

    hit = 0

    for item in catalog:

        value = item.get(key)

        if not isinstance(value, str):
            continue

        stem = Path(value).stem

        if stem in pdf_ids:
            hit += 1

    print(f"{key:25} -> {hit}")

    if hit > best_match:
        best_match = hit
        best_key = key

print()
print("=" * 80)
print("BEST FIELD")
print("=" * 80)

print(best_key, best_match)

print()
print("=" * 80)
print("LOOK FOR ANY UUID IN JSON")
print("=" * 80)

found = 0

def walk(obj):

    global found

    if isinstance(obj, dict):
        for v in obj.values():
            walk(v)

    elif isinstance(obj, list):
        for v in obj:
            walk(v)

    elif isinstance(obj, str):

        if len(obj) == 32 and obj in pdf_ids:

            print(obj)

            found += 1

            if found >= 30:
                raise SystemExit

walk(catalog)

print()
print("=" * 80)
print("DONE")
print("=" * 80)
