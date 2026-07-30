#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
#
# PR-2.16B
#
# Architecture Inventory Builder
#
# READ ONLY
#
# Purpose
#
#   Build a canonical inventory of the repository.
#
#   This script NEVER modifies source code.
#
#   Output:
#
#       reports/architecture_inventory.json
#       reports/architecture_inventory.csv
#       reports/architecture_inventory.md
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

[[ -d "$ROOT/tools/architecture" ]] \
    || die "tools/architecture not found"

[[ -f "$ROOT/tools/architecture/inventory.py" ]] \
    || die "inventory.py not found"

################################################################################
# HEADER
################################################################################

log "============================================================"
log "DELBot Architecture Inventory"
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

log "Generating inventory"

"$PYTHON" \
    -m tools.architecture.inventory

echo

################################################################################
# VERIFY REPORTS
################################################################################

FILES=(

architecture_inventory.json
architecture_inventory.csv
architecture_inventory.md

)

echo

log "Checking reports"

for file in "${FILES[@]}"
do

    PATH_FILE="$REPORT_DIR/$file"

    if [[ -f "$PATH_FILE" ]]; then

        SIZE=$(stat -c%s "$PATH_FILE")

        printf "  %-35s %12s bytes\n" "$file" "$SIZE"

    else

        printf "  %-35s %12s\n" "$file" "MISSING"

    fi

done

echo

ok "============================================================"
ok "Inventory Finished"
ok "============================================================"

echo
