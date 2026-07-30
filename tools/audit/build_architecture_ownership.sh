#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.16D
#
# Architecture Ownership Builder
#
# READ ONLY
#
# Output
#
#   reports/architecture_ownership.json
#   reports/architecture_ownership.csv
#   reports/architecture_ownership.md
#
# ==============================================================================

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PYTHON="$ROOT/.venv/bin/python"
else
    PYTHON="python3"
fi

REPORT_DIR="$ROOT/reports"
mkdir -p "$REPORT_DIR"

echo "============================================================"
echo "DELBot Architecture Ownership"
echo "============================================================"
echo

echo "Repository : $ROOT"
echo "Python     : $PYTHON"
echo

FAILED=0

while IFS= read -r file
do
    "$PYTHON" -m py_compile "$file" || FAILED=1
done < <(
find tools/architecture -name "*.py" | sort
)

[[ "$FAILED" == "0" ]] || {
    echo "Compile failed."
    exit 1
}

echo "Compile PASS"
echo

echo "Generating ownership..."

"$PYTHON" -m tools.architecture.ownership

echo

for f in \
architecture_ownership.json \
architecture_ownership.csv \
architecture_ownership.md
do

if [[ -f reports/$f ]]; then
    printf "%-40s %10d bytes\n" \
    "$f" \
    "$(stat -c%s reports/$f)"
else
    printf "%-40s %10s\n" "$f" MISSING
fi

done

echo
echo "Finished."

