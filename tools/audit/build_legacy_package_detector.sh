#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.17C
#
# Legacy Package Detector
#
# READ ONLY
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
echo "DELBot Legacy Package Detector"
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

"$PYTHON" -m tools.architecture.legacy_package_detector

echo

for f in \
legacy_package_detector.json \
legacy_package_detector.csv \
legacy_package_detector.md
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
