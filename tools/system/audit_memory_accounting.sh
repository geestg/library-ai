#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

REPORT_DIR="$ROOT/runtime/system_report"

mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/memory_accounting_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$REPORT")
exec 2>&1

echo "=================================================="
echo "MEMORY ACCOUNTING"
echo "=================================================="

echo
echo "===== FREE ====="
free -h

echo
echo "===== MEMINFO ====="

grep -E \
'MemTotal|MemFree|MemAvailable|Buffers|Cached|AnonPages|Mapped|Shmem|Slab|KernelStack|PageTables|AnonHugePages|HugePages|Hugepagesize|CommitLimit|Committed_AS|Vmalloc' \
/proc/meminfo

echo
echo "===== SHARED MEMORY ====="

df -h /dev/shm || true

echo

ipcs -m || true

echo
echo "===== TMPFS ====="

mount | grep tmpfs || true

echo
echo "===== CGROUP ====="

cat /proc/self/cgroup || true

echo
echo "===== CGROUP MEMORY ====="

find /sys/fs/cgroup \
-name memory.current \
-exec sh -c 'echo === {}; cat {}' \; 2>/dev/null

echo
echo "===== CGROUP LIMIT ====="

find /sys/fs/cgroup \
-name memory.max \
-exec sh -c 'echo === {}; cat {}' \; 2>/dev/null

echo
echo "===== HUGEPAGES ====="

grep Huge /proc/meminfo

echo
echo "===== MAPPED FILES ====="

grep -E 'Mapped|AnonPages|Shmem' /proc/meminfo

echo
echo "===== VIRTUAL MEMORY ====="

vmstat -s

echo
echo "===== REPORT ====="

echo "$REPORT"
