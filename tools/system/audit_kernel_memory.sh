#!/usr/bin/env bash
#
# ============================================================
# DELBot
# Kernel Memory Audit
#
# Audit anonymous memory dari seluruh proses
# Menggunakan /proc/*/smaps_rollup (lebih cepat)
#
# Author : DELBot
# ============================================================

set -euo pipefail

RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"
RESET="\033[0m"

printf "\n${CYAN}"
echo "============================================================"
echo "        DELBOT KERNEL MEMORY AUDIT"
echo "============================================================"
printf "${RESET}\n"

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}"
    echo "ERROR:"
    echo
    echo "Harus dijalankan menggunakan sudo/root."
    echo
    echo "Contoh:"
    echo
    echo "sudo bash tools/system/audit_kernel_memory.sh"
    echo
    printf "${RESET}"
    exit 1
fi

TMP=$(mktemp)

printf "%-8s %-30s %12s %12s %12s %12s\n" \
PID NAME ANON_MB PRIVATE_MB SHARED_MB RSS_MB

echo "-----------------------------------------------------------------------------------------------"

TOTAL_ANON=0
TOTAL_PRIVATE=0
TOTAL_SHARED=0
TOTAL_RSS=0

for smaps in /proc/[0-9]*/smaps_rollup
do
    PID=$(echo "$smaps" | cut -d/ -f3)

    [[ -r "$smaps" ]] || continue

    NAME=$(tr '\0' ' ' < /proc/$PID/cmdline 2>/dev/null | cut -c1-28)

    if [[ -z "$NAME" ]]; then
        NAME=$(cat /proc/$PID/comm 2>/dev/null || echo unknown)
    fi

    ANON=$(awk '/Anonymous:/ {print $2}' "$smaps")
    PRIVATE=$(awk '/Private_Dirty:/ {print $2}' "$smaps")
    SHARED=$(awk '/Shared_Dirty:/ {print $2}' "$smaps")
    RSS=$(awk '/Rss:/ {print $2}' "$smaps")

    ANON=${ANON:-0}
    PRIVATE=${PRIVATE:-0}
    SHARED=${SHARED:-0}
    RSS=${RSS:-0}

    TOTAL_ANON=$((TOTAL_ANON+ANON))
    TOTAL_PRIVATE=$((TOTAL_PRIVATE+PRIVATE))
    TOTAL_SHARED=$((TOTAL_SHARED+SHARED))
    TOTAL_RSS=$((TOTAL_RSS+RSS))

    printf "%-8s %-30s %12d %12d %12d %12d\n" \
        "$PID" \
        "$NAME" \
        $((ANON/1024)) \
        $((PRIVATE/1024)) \
        $((SHARED/1024)) \
        $((RSS/1024)) \
        >> "$TMP"
done

sort -k3 -nr "$TMP"

echo
echo "============================================================"
echo "TOTAL"
echo "============================================================"

printf "Anonymous      : %12d MB\n" $((TOTAL_ANON/1024))
printf "Private Dirty  : %12d MB\n" $((TOTAL_PRIVATE/1024))
printf "Shared Dirty   : %12d MB\n" $((TOTAL_SHARED/1024))
printf "RSS            : %12d MB\n" $((TOTAL_RSS/1024))

echo
echo "============================================================"
echo "SYSTEM MEMORY"
echo "============================================================"

grep -E 'MemTotal|MemFree|MemAvailable|Cached|Buffers|AnonPages|Shmem|Slab|KernelStack|PageTables|SReclaimable|SUnreclaim' /proc/meminfo

echo
echo "============================================================"
echo "CGROUP"
echo "============================================================"

for f in \
/sys/fs/cgroup/memory.current \
/sys/fs/cgroup/memory.max
do
    if [[ -f "$f" ]]; then
        printf "%-25s : " "$(basename "$f")"
        cat "$f"
    fi
done

echo
echo "============================================================"
echo "KERNEL SLAB"
echo "============================================================"

if command -v slabtop >/dev/null
then
    slabtop -o | head -25
else
    echo "slabtop tidak tersedia."
fi

echo
echo "============================================================"
echo "VMSTAT"
echo "============================================================"

grep -E \
'anon|file|slab|unevictable|pgfault|pgmajfault|thp|nr_' \
/proc/vmstat | head -80

echo
echo "============================================================"
echo "TRANSPARENT HUGE PAGE"
echo "============================================================"

if [[ -f /sys/kernel/mm/transparent_hugepage/enabled ]]; then
    cat /sys/kernel/mm/transparent_hugepage/enabled
fi

echo
echo "============================================================"
echo "HUGEPAGES"
echo "============================================================"

grep Huge /proc/meminfo

echo
echo "============================================================"
echo "NUMA"
echo "============================================================"

if command -v numastat >/dev/null
then
    numastat
fi

echo
echo "============================================================"
echo "TOP 20 MAP SIZE"
echo "============================================================"

sort -k6 -nr "$TMP" | head -20

rm "$TMP"

echo
echo "============================================================"
echo "AUDIT COMPLETE"
echo "============================================================"