#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.16E
#
# Duplicate Candidate Builder
#
# READ ONLY
#
# Output
#
#   reports/duplicate_candidates.json
#   reports/duplicate_candidates.csv
#   reports/duplicate_candidates.md
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

echo "============================================================"
echo "DELBot Duplicate Candidate Detection"
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

echo "Detecting duplicate candidates..."

"$PYTHON" -m tools.architecture.duplicate

echo

for f in \
duplicate_candidates.json \
duplicate_candidates.csv \
duplicate_candidates.md
do

if [[ -f reports/$f ]]; then

printf "%-40s %10d bytes\n" \
"$f" \
"$(stat -c%s reports/$f)"

else

printf "%-40s %10s\n" \
"$f" \
"MISSING"

fi

done

echo
echo "Finished."

