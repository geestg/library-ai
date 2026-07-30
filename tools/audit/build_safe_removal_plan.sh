#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PYTHON="$ROOT/.venv/bin/python"
else
    PYTHON="python3"
fi

echo "============================================================"
echo "DELBot Safe Removal Planner"
echo "============================================================"
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

"$PYTHON" -m tools.architecture.safe_removal_planner

echo

for f in \
safe_removal_plan.json \
safe_removal_plan.csv \
safe_removal_plan.md
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
