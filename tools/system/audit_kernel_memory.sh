#!/usr/bin/env bash

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

REPORT_DIR="$ROOT/runtime/system_report"

mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/kernel_memory_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$REPORT")
exec 2>&1

echo "============================================================"
echo "DELBOT KERNEL MEMORY AUDIT"
echo "============================================================"

echo
date

echo
hostname

echo
echo "============================================================"
echo "SYSTEM MEMORY"
echo "============================================================"

grep -E \
'MemTotal|MemFree|MemAvailable|AnonPages|Mapped|Cached|Slab|KernelStack|PageTables|AnonHugePages|HugePages|Committed_AS' \
/proc/meminfo

echo
echo "============================================================"
echo "TOP PROCESS MEMORY"
echo "============================================================"

printf "%-8s %-10s %-10s %-10s %-10s %s\n" \
PID RSS_MB ANON_MB PRIVATE_MB SHARED_MB CMD

TMP=$(mktemp)

for PROC in /proc/[0-9]*; do

    PID=$(basename "$PROC")

    [[ -r "$PROC/status" ]] || continue

    RSS=0
    ANON=0
    PRIVATE=0
    SHARED=0

    while read -r KEY VALUE UNIT; do

        case "$KEY" in

            VmRSS:)
                RSS=$VALUE
                ;;

            RssAnon:)
                ANON=$VALUE
                ;;

        esac

    done < "$PROC/status"

    if [[ -r "$PROC/smaps_rollup" ]]; then

        PRIVATE=$(
            awk '
            /Private_Clean:/ {x+=$2}
            /Private_Dirty:/ {x+=$2}
            END{print x+0}
            ' "$PROC/smaps_rollup" 2>/dev/null || echo 0
        )

        SHARED=$(
            awk '
            /Shared_Clean:/ {x+=$2}
            /Shared_Dirty:/ {x+=$2}
            END{print x+0}
            ' "$PROC/smaps_rollup" 2>/dev/null || echo 0
        )

    fi

    CMD=$(tr '\0' ' ' < "$PROC/cmdline" 2>/dev/null)

    [[ -z "$CMD" ]] && CMD=$(cat "$PROC/comm" 2>/dev/null)

    printf "%-8s %-10.1f %-10.1f %-10.1f %-10.1f %s\n" \
        "$PID" \
        "$(awk "BEGIN{print $RSS/1024}")" \
        "$(awk "BEGIN{print $ANON/1024}")" \
        "$(awk "BEGIN{print $PRIVATE/1024}")" \
        "$(awk "BEGIN{print $SHARED/1024}")" \
        "$CMD" >> "$TMP"

done

sort -k3 -nr "$TMP" | head -100

echo
echo "============================================================"
echo "TOTAL"
echo "============================================================"

awk '

{

rss+=$2
anon+=$3
priv+=$4
shared+=$5

}

END{

printf "RSS      : %.2f GB\n",rss/1024
printf "ANON     : %.2f GB\n",anon/1024
printf "PRIVATE  : %.2f GB\n",priv/1024
printf "SHARED   : %.2f GB\n",shared/1024

}

' "$TMP"

echo
echo "============================================================"
echo "TOP ANON HUGEPAGES"
echo "============================================================"

printf "%-8s %-12s %s\n" PID HUGE_MB CMD

TMP2=$(mktemp)

for PROC in /proc/[0-9]*; do

    PID=$(basename "$PROC")

    [[ -r "$PROC/smaps_rollup" ]] || continue

    HUGE=$(
        awk '
        /AnonHugePages:/ {print $2}
        ' "$PROC/smaps_rollup" 2>/dev/null || echo 0
    )

    HUGE=${HUGE:-0}

    CMD=$(tr '\0' ' ' < "$PROC/cmdline" 2>/dev/null)

    [[ -z "$CMD" ]] && CMD=$(cat "$PROC/comm" 2>/dev/null)

    printf "%-8s %-12.1f %s\n" \
        "$PID" \
        "$(awk "BEGIN{print $HUGE/1024}")" \
        "$CMD" >> "$TMP2"

done

sort -k2 -nr "$TMP2" | head -60

echo
echo "============================================================"
echo "OPEN DELETED FILES"
echo "============================================================"

if command -v lsof >/dev/null 2>&1; then

    lsof +L1 2>/dev/null | head -80
fi

echo
echo "============================================================"
echo "VMSTAT"
echo "============================================================"

vmstat -s

echo
echo "============================================================"
echo "REPORT"
echo "============================================================"

echo "$REPORT"

rm -f "$TMP" "$TMP2"