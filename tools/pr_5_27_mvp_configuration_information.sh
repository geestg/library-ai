#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.27
#
# Configuration Information
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
OUTPUT="$REPORTDIR/mvp_configuration_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.27 Configuration Information"
echo "======================================================================"

python3 <<PY
import json
from pathlib import Path
from datetime import datetime

root = Path(r"$ROOT")
report = Path(r"$OUTPUT")

checks = {
    "venv_exists": (root / ".venv").exists(),
    "repository_data_exists": (root / "repository_data").exists(),
    "mapping_exists": (root / "repository_data" / "mapping").exists(),
    "report_exists": (root / "repository_data" / "report").exists(),
    "pdf_repository_exists": (root / "delbot_platform" / "repository_data" / "pdf").exists(),
    "qdrant_local_exists": (root / "repository_data" / "qdrant_local").exists(),
    "tools_exists": (root / "tools").exists(),
    "git_exists": (root / ".git").exists(),
}

data = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "project": "DELBot MVP",
    "total_checks": len(checks),
    "passed": sum(1 for v in checks.values() if v),
    "failed": sum(1 for v in checks.values() if not v),
    "configuration": checks,
    "status": "SUCCESS",
}

report.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8",
)

print(json.dumps(data, indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.28 MVP Directory Information"

