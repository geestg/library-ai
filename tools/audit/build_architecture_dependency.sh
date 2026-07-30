#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.16C
#
# Architecture Dependency Builder
#
# READ ONLY
#
# Purpose
#
#   Build canonical dependency graph.
#
#   Output
#
#       reports/architecture_dependency.json
#       reports/architecture_dependency.csv
#       reports/architecture_dependency.md
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
# COLORS
################################################################################

CYAN="\033[36m"
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

log() {
    printf "${CYAN}%s${RESET}\n" "$1"
}

ok() {
    printf "${GREEN}%s${RESET}\n" "$1"
}

die() {
    printf "${RED}%s${RESET}\n" "$1"
    exit 1
}

################################################################################
# VERIFY
################################################################################

[[ -f "$ROOT/tools/architecture/dependency.py" ]] \
    || die "dependency.py not found"

################################################################################
# HEADER
################################################################################

log "============================================================"
log "DELBot Architecture Dependency"
log "============================================================"

echo

echo "Repository"

echo "    $ROOT"

echo

echo "Python"

echo "    $PYTHON"

echo

################################################################################
# COMPILE
################################################################################

log "Compile"

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

[[ "$FAILED" == "0" ]] \
    || die "Compile failed"

ok "Compile PASS"

echo

################################################################################
# RUN
################################################################################

log "Generating dependency graph"

"$PYTHON" \
    -m tools.architecture.dependency

echo

################################################################################
# VERIFY
################################################################################

FILES=(

architecture_dependency.json
architecture_dependency.csv
architecture_dependency.md

)

log "Checking reports"

for file in "${FILES[@]}"
do

    TARGET="$REPORT_DIR/$file"

    if [[ -f "$TARGET" ]]; then

        SIZE=$(stat -c%s "$TARGET")

        printf "  %-35s %12s bytes\n" "$file" "$SIZE"

    else

        printf "  %-35s %12s\n" "$file" "MISSING"

    fi

done

echo

ok "============================================================"
ok "Dependency Finished"
ok "============================================================"

echo

