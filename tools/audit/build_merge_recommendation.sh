#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.16F
#
# Merge Recommendation Builder
#
# READ ONLY
#
# Output
#
#   reports/merge_recommendation.json
#   reports/merge_recommendation.csv
#   reports/merge_recommendation.md
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
# REPORTS
################################################################################

REPORT_DIR="$ROOT/reports"

mkdir -p "$REPORT_DIR"

################################################################################
# HEADER
################################################################################

echo "============================================================"
echo "DELBot Merge Recommendation"
echo "============================================================"
echo

echo "Repository : $ROOT"
echo "Python     : $PYTHON"
echo

################################################################################
# VERIFY
################################################################################

[[ -f tools/architecture/merge_recommendation.py ]] || {

    echo "merge_recommendation.py not found"

    exit 1

}

################################################################################
# COMPILE
################################################################################

FAILED=0

while IFS= read -r file
do

    "$PYTHON" -m py_compile "$file" || FAILED=1

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

echo "Generating merge recommendation..."

echo

"$PYTHON" \
    -m tools.architecture.merge_recommendation

################################################################################
# VERIFY REPORTS
################################################################################

echo

FILES=(

merge_recommendation.json
merge_recommendation.csv
merge_recommendation.md

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
