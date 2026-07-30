#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.17A
#
# Architecture Index Builder
#
# READ ONLY
#
# Output
#
#   reports/architecture_index.json
#   reports/architecture_index.csv
#   reports/architecture_index.md
#
# ==============================================================================

set -Eeuo pipefail

################################################################################
# ROOT
################################################################################

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT"

################################################################################
# PYTHON
################################################################################

if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PYTHON="$ROOT/.venv/bin/python"
else
    PYTHON="python3"
fi

################################################################################
# REPORT DIRECTORY
################################################################################

REPORT_DIR="$ROOT/reports"

mkdir -p "$REPORT_DIR"

################################################################################
# VERIFY
################################################################################

[[ -f "$ROOT/tools/architecture/index.py" ]] || {
    echo "index.py not found"
    exit 1
}

################################################################################
# HEADER
################################################################################

echo "============================================================"
echo "DELBot Architecture Index"
echo "============================================================"
echo

echo "Repository : $ROOT"
echo "Python     : $PYTHON"
echo

################################################################################
# COMPILE
################################################################################

FAILED=0

while IFS= read -r file
do

    if ! "$PYTHON" -m py_compile "$file"; then
        FAILED=1
    fi

done < <(

find tools/architecture \
    -name "*.py" \
    | sort

)

[[ "$FAILED" == "0" ]] || {

    echo
    echo "Compile failed."
    exit 1

}

echo "Compile PASS"
echo

################################################################################
# RUN
################################################################################

echo "Generating architecture index..."
echo

"$PYTHON" \
    -m tools.architecture.index

################################################################################
# VERIFY REPORTS
################################################################################

echo

FILES=(

architecture_index.json
architecture_index.csv
architecture_index.md

)

for file in "${FILES[@]}"
do

    TARGET="$REPORT_DIR/$file"

    if [[ -f "$TARGET" ]]; then

        printf "%-40s %12d bytes\n" \
            "$file" \
            "$(stat -c%s "$TARGET")"

    else

        printf "%-40s %12s\n" \
            "$file" \
            "MISSING"

    fi

done

echo
echo "============================================================"
echo "Finished"
echo "============================================================"
echo
