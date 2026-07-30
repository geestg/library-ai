#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

REPORT_DIR="$ROOT/runtime/system_report"

mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/process_memory_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$REPORT")
exec 2>&1

echo "====================================================="
echo "PROCESS MEMORY AUDIT"
echo "====================================================="

printf "%-8s %-10s %-12s %-12s %s\n" \
PID RSS_MB PSS_MB SWAP_MB CMD

echo

for pid in $(ls /proc | grep '^[0-9]'); do

    if [[ ! -r /proc/$pid/status ]]; then
        continue
    fi

    cmd=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)

    [[ -z "$cmd" ]] && cmd=$(cat /proc/$pid/comm 2>/dev/null)

    rss=0
    pss=0
    swap=0

    if [[ -r /proc/$pid/smaps_rollup ]]; then

        rss=$(awk '/Rss:/ {print $2}' /proc/$pid/smaps_rollup)

        pss=$(awk '/Pss:/ {print $2}' /proc/$pid/smaps_rollup)

        swap=$(awk '/Swap:/ {print $2}' /proc/$pid/smaps_rollup)

    fi

    printf "%-8s %-10.1f %-12.1f %-12.1f %s\n" \
        "$pid" \
        "$(awk "BEGIN{print $rss/1024}")" \
        "$(awk "BEGIN{print $pss/1024}")" \
        "$(awk "BEGIN{print $swap/1024}")" \
        "$cmd"

done | sort -k2 -nr | head -80

echo
echo "====================================================="
echo "TOTAL RSS"
echo "====================================================="

awk '

NR>2{

rss+=$2

pss+=$3

swap+=$4

}

END{

printf "RSS : %.2f GB\n",rss/1024

printf "PSS : %.2f GB\n",pss/1024

printf "SWAP: %.2f GB\n",swap/1024

}

' "$REPORT"

echo

echo "Report"

echo "$REPORT"
