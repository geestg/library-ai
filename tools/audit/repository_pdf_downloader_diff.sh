#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/workspace/delbot"
cd "$ROOT"

LEFT="delbot_platform/repository/download/downloader.py"
RIGHT="delbot_platform/repository/download/pdf_downloader.py"

echo "============================================================"
echo "DELBot MVP"
echo "Repository PDFDownloader Diff"
echo "============================================================"
echo

for file in "$LEFT" "$RIGHT"
do
    [[ -f "$file" ]] || {
        echo "Missing: $file"
        exit 1
    }
done

echo "------------------------------------------------------------"
echo "File Information"
echo "------------------------------------------------------------"

wc -l "$LEFT" "$RIGHT"

echo
echo "------------------------------------------------------------"
echo "SHA256"
echo "------------------------------------------------------------"

sha256sum "$LEFT" "$RIGHT"

echo
echo "------------------------------------------------------------"
echo "Unified Diff"
echo "------------------------------------------------------------"

diff -u "$LEFT" "$RIGHT" || true

echo
echo "Done."

