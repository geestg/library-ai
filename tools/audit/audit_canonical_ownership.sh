#!/usr/bin/env bash
# ==============================================================================
#
# DELBot
# Architecture Audit Framework
#
# PR-2.16A
#
# Execute architecture audit as Python packages.
#
# READ ONLY
#
# ==============================================================================

set -Eeuo pipefail

################################################################################
# ROOT
################################################################################

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT"

export PYTHONPATH="$ROOT"

REPORT_DIR="$ROOT/reports"

mkdir -p "$REPORT_DIR"

################################################################################
# COLORS
################################################################################

RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"
RESET="\033[0m"

log() {
    printf "${CYAN}%s${RESET}\n" "$1"
}

ok() {
    printf "${GREEN}%s${RESET}\n" "$1"
}

warn() {
    printf "${YELLOW}%s${RESET}\n" "$1"
}

die() {
    printf "${RED}%s${RESET}\n" "$1"
    exit 1
}

################################################################################
# PYTHON
################################################################################

PYTHON="python"

if [ -x "$ROOT/.venv/bin/python" ]; then
    PYTHON="$ROOT/.venv/bin/python"
fi

################################################################################
# HEADER
################################################################################

log "============================================================"
log "DELBot Architecture Audit"
log "============================================================"

echo

echo "Repository"

echo "  $ROOT"

echo

echo "Python"

echo "  $PYTHON"

echo

################################################################################
# VERIFY
################################################################################

MODULE_DIR="$ROOT/tools/architecture"

[ -d "$MODULE_DIR" ] || die "Missing tools/architecture"

MODULES=(
scanner
inventory
dependency
graph
graph_filter
filter
metrics
resolver
layer
pipeline
doctor
models
circular
)

log "Checking modules"

for module in "${MODULES[@]}"
do

    FILE="$MODULE_DIR/${module}.py"

    [ -f "$FILE" ] || die "Missing $module.py"

    ok "OK  $module"

done

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
find "$MODULE_DIR" \
-type f \
-name "*.py" \
| sort
)

[ "$FAILED" -eq 0 ] || die "Compile failed"

ok "Compile PASS"

echo

################################################################################
# RUN MODULE
################################################################################

run_module() {

    local module="$1"

    log "Running ${module}"

    "$PYTHON" \
        -m "tools.architecture.${module}"

    echo
}

################################################################################
# EXECUTION
################################################################################

run_module inventory
run_module dependency
run_module graph
run_module pipeline
run_module metrics
run_module doctor

################################################################################
# DONE
################################################################################

ok "============================================================"
ok "Architecture Audit Finished"
ok "============================================================"

echo

find "$REPORT_DIR" \
-maxdepth 1 \
-type f \
| sort

echo