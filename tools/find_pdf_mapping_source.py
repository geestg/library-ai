from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEARCH_DIRS = [
    ROOT / "delbot_platform",
    ROOT / "repository",
    ROOT / "datasets",
]

JSON_FILES = []

for directory in SEARCH_DIRS:
    if directory.exists():
        JSON_FILES.extend(directory.rglob("*.json"))

print("=" * 80)
print("JSON FILES")
print("=" * 80)

for f in sorted(JSON_FILES):
    print(f.relative_to(ROOT))

print()
print("=" * 80)
print("SCAN FOR UUID REFERENCES")
print("=" * 80)

interesting = []

for f in sorted(JSON_FILES):

    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue

    text = json.dumps(data)

    score = 0

    if "0087b57cdff943ca8b4aca6f5f80e304" in text:
        score += 1

    if ".pdf" in text.lower():
        score += 1

    if "pdf_path" in text:
        score += 1

    if "document_id" in text:
        score += 1

    if score:
        interesting.append((score, f))

interesting.sort(reverse=True)

for score, f in interesting:
    print(f"[score={score}] {f.relative_to(ROOT)}")

print()

print("=" * 80)
print("INSPECT FIRST MATCHES")
print("=" * 80)

for _, f in interesting[:10]:

    print()
    print("-" * 80)
    print(f.relative_to(ROOT))
    print("-" * 80)

    try:
        obj = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(e)
        continue

    if isinstance(obj, list):

        print("TYPE : list")
        print("LEN  :", len(obj))

        if obj:
            first = obj[0]

            if isinstance(first, dict):

                print("FIELDS")

                for k in first.keys():
                    print(" ", k)

                print()
                print("FIRST RECORD")

                for k, v in first.items():

                    s = str(v)

                    if len(s) > 150:
                        s = s[:150] + "..."

                    print(f"{k}: {s}")

    elif isinstance(obj, dict):

        print("TYPE : dict")
        print("KEYS :")

        for k in obj.keys():
            print(" ", k)

print()
print("=" * 80)
print("DONE")
print("=" * 80)
