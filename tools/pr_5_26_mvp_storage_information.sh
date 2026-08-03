#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.26
#
# Storage Information
#
# SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

REPORTDIR="$ROOT/repository_data/report"
OUTPUT="$REPORTDIR/mvp_storage_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.26 Storage Information"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

root=pathlib.Path(r"$ROOT")

def size_mb(path):
    if not path.exists():
        return 0.0
    total=0
    for f in path.rglob("*"):
        if f.is_file():
            try:
                total+=f.stat().st_size
            except Exception:
                pass
    return round(total/(1024*1024),2)

pdf_dir=root/"delbot_platform"/"repository_data"/"pdf"
map_dir=root/"repository_data"/"mapping"
report_dir=root/"repository_data"/"report"
export_dir=root/"repository_data"/"mvp_export"
qdrant_dir=root/"repository_data"/"qdrant_local"

data={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "storage":{
        "pdf_repository":{
            "exists":pdf_dir.exists(),
            "size_mb":size_mb(pdf_dir)
        },
        "mapping":{
            "exists":map_dir.exists(),
            "size_mb":size_mb(map_dir)
        },
        "report":{
            "exists":report_dir.exists(),
            "size_mb":size_mb(report_dir)
        },
        "qdrant_local":{
            "exists":qdrant_dir.exists(),
            "size_mb":size_mb(qdrant_dir)
        },
        "mvp_export":{
            "exists":export_dir.exists(),
            "size_mb":size_mb(export_dir)
        }
    },
    "status":"SUCCESS"
}

pathlib.Path(r"$OUTPUT").write_text(
    json.dumps(data,indent=2),
    encoding="utf-8"
)

print(json.dumps({
    "project":data["project"],
    "storage_checked":len(data["storage"]),
    "status":data["status"]
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.27 MVP Configuration Information"

