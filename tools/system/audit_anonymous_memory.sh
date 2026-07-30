#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

REPORT_DIR="$ROOT/runtime/system_report"

mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/anonymous_memory_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$REPORT")
exec 2>&1

echo "=========================================================="
echo "ANONYMOUS MEMORY AUDIT"
echo "=========================================================="

printf "%-8s %-10s %-10s %-10s %s\n" \
PID RSS_MB ANON_MB SHMEM_MB CMD

echo

for pid in /proc/[0-9]*; do

    pid=$(basename "$pid")

    [[ -r /proc/$pid/status ]] || continue

    rss=0
    anon=0
    shmem=0

    while read -r key value unit; do

        case "$key" in

            VmRSS:)
                rss=$value
                ;;

            RssAnon:)
                anon=$value
                ;;

            RssShmem:)
                shmem=$value
                ;;

        esac

    done < /proc/$pid/status

    cmd=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)

    [[ -z "$cmd" ]] && cmd=$(cat /proc/$pid/comm 2>/dev/null)

    printf "%-8s %-10.1f %-10.1f %-10.1f %s\n" \
        "$pid" \
        "$(awk "BEGIN{print $rss/1024}")" \
        "$(awk "BEGIN{print $anon/1024}")" \
        "$(awk "BEGIN{print $shmem/1024}")" \
        "$cmd"

done | sort -k3 -nr | head -120

echo

echo "=========================================================="

echo "TOTAL ANON"

echo "=========================================================="

awk '

NR>2{

rss+=$2

anon+=$3

shm+=$4

}

END{

printf "RSS  : %.2f GB\n",rss/1024

printf "ANON : %.2f GB\n",anon/1024

printf "SHMEM: %.2f GB\n",shm/1024

}

' "$REPORT"

echo

echo "$REPORT"
