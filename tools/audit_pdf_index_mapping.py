from __future__ import annotations

import json
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[1]

META = ROOT / "delbot_platform/repository_data/metadata"

FILES = [
    "pdf_index.json",
    "repository_catalog.json",
    "skripsi_dataset.json",
]

for name in FILES:

    path = META / name

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    if not path.exists():
        print("NOT FOUND")
        continue

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print("LOAD FAILED:", e)
        continue

    print("TYPE :", type(data).__name__)

    if isinstance(data, list):
        print("LEN  :", len(data))

        if data:
            first = data[0]

            print("\nFIRST TYPE")
            print(type(first).__name__)

            if isinstance(first, dict):
                print("\nFIELDS")
                for k in first.keys():
                    print("-", k)

                print("\nFIRST RECORD")
                pprint(first, width=120)

    elif isinstance(data, dict):

        print("KEY COUNT :", len(data))

        keys = list(data.keys())

        print("\nFIRST 50 KEYS")

        for k in keys[:50]:
            print(k)

        if keys:

            sample = data[keys[0]]

            print("\nFIRST VALUE TYPE")
            print(type(sample).__name__)

            print("\nFIRST VALUE")

            pprint(sample, width=120)

print("\n" + "=" * 80)
print("SEARCH UUID-LIKE VALUES")
print("=" * 80)

import re

uuid_re = re.compile(r"^[0-9a-f]{32}$")

for name in FILES:

    path = META / name

    if not path.exists():
        continue

    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue

    found = []

    def walk(x):

        if isinstance(x, dict):
            for v in x.values():
                walk(v)

        elif isinstance(x, list):
            for v in x:
                walk(v)

        elif isinstance(x, str):
            if uuid_re.fullmatch(x):
                found.append(x)

    walk(obj)

    print("\n", name)
    print("UUID FOUND :", len(found))

    for v in found[:30]:
        print(v)

print("\nDONE")
