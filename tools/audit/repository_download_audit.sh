#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/workspace/delbot"
cd "$ROOT"

echo "============================================================"
echo "DELBot MVP"
echo "Repository Download Audit"
echo "============================================================"
echo

FILES=(
"delbot_platform/repository/download/downloader.py"
"delbot_platform/repository/download/pdf_downloader.py"
"delbot_platform/repository/download/result.py"
"delbot_platform/repository/download/__init__.py"
)

for file in "${FILES[@]}"
do

echo
echo "============================================================"
echo "$file"
echo "============================================================"

if [[ ! -f "$file" ]]; then
    echo "MISSING"
    continue
fi

echo
echo "----- Lines -----"
wc -l "$file"

echo
echo "----- Imports -----"
grep -nE "^from |^import " "$file" || true

echo
echo "----- Classes -----"
grep -n "^class " "$file" || true

echo
echo "----- Functions -----"
grep -nE "^def |^async def " "$file" || true

done

echo
echo "============================================================"
echo "Repository Download Tree"
echo "============================================================"

tree delbot_platform/repository/download

echo
echo "Done."
