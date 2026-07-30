from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

meta_dir = ROOT / "delbot_platform/repository_data/metadata"
pdf_dir = ROOT / "delbot_platform/repository_data/pdf"

print("=" * 60)
print("CATALOG")
print("=" * 60)

catalog = json.loads(
    (meta_dir / "repository_catalog.json").read_text(
        encoding="utf-8"
    )
)

print("catalog records :", len(catalog))

print()
print("=" * 60)
print("PDF FILES")
print("=" * 60)

pdf_files = sorted(pdf_dir.glob("*.pdf"))

print("pdf files :", len(pdf_files))

pdf_names = {
    p.stem
    for p in pdf_files
}

print()
print("=" * 60)
print("FIELDS")
print("=" * 60)

sample = catalog[0]

for k in sample.keys():
    print(k)

print()
print("=" * 60)
print("SEARCH UUID FIELDS")
print("=" * 60)

possible = set()

for record in catalog:

    for key, value in record.items():

        if isinstance(value, str):

            if value in pdf_names:
                possible.add(key)

        elif isinstance(value, dict):

            for k2, v2 in value.items():

                if isinstance(v2, str):

                    if v2 in pdf_names:
                        possible.add(f"{key}.{k2}")

print("candidate fields:")

if possible:
    for x in sorted(possible):
        print(" ", x)
else:
    print(" NONE")

print()
print("=" * 60)
print("SEARCH PDF PATH")
print("=" * 60)

count = 0

for record in catalog:

    for key, value in record.items():

        if isinstance(value, str):

            if ".pdf" in value.lower():
                count += 1
                print(key, "=>", value)

        elif isinstance(value, dict):

            for k2, v2 in value.items():

                if isinstance(v2, str):

                    if ".pdf" in v2.lower():
                        count += 1
                        print(f"{key}.{k2} => {v2}")

print()

print("pdf path entries:", count)

print()
print("=" * 60)
print("MATCH COUNT")
print("=" * 60)

matched = 0

for record in catalog:

    found = False

    def walk(obj):

        nonlocal found

        if found:
            return

        if isinstance(obj, dict):

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):

            for v in obj:
                walk(v)

        elif isinstance(obj, str):

            if obj in pdf_names:
                found = True

    walk(record)

    if found:
        matched += 1

print("records mapped to existing pdf :", matched)

print()
print("=" * 60)
print("FIRST 5 PDF FILES")
print("=" * 60)

for p in pdf_files[:5]:
    print(p.name)

print()
print("=" * 60)
print("FIRST RECORD")
print("=" * 60)

print(
    json.dumps(
        sample,
        indent=2,
        ensure_ascii=False
    )[:6000]
)
