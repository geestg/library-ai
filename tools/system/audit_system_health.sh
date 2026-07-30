#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORT_DIR="$ROOT/runtime/system_report"

mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/system_health_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$REPORT")
exec 2>&1

echo "=========================================================="
echo "DELBOT SYSTEM HEALTH AUDIT"
echo "=========================================================="

echo
echo "DATE"
date

echo
echo "HOST"
hostname

echo
echo "UPTIME"
uptime

echo
echo "=========================================================="
echo "MEMORY"
echo "=========================================================="

free -h

echo
grep -E "MemTotal|MemFree|MemAvailable|Cached|Buffers|Slab|SReclaimable|SUnreclaim" /proc/meminfo

echo
echo "=========================================================="
echo "TOP MEMORY PROCESS"
echo "=========================================================="

ps -eo pid,ppid,user,%mem,rss,vsz,cmd \
| sort -k4 -nr \
| head -40

echo
echo "=========================================================="
echo "TOP CPU"
echo "=========================================================="

ps -eo pid,ppid,user,%cpu,%mem,cmd \
| sort -k4 -nr \
| head -40

echo
echo "=========================================================="
echo "ZOMBIE PROCESS"
echo "=========================================================="

ps -eo stat,pid,ppid,cmd \
| awk '$1 ~ /^Z/'

echo
echo "Zombie Count"

ps -eo stat \
| grep '^Z' \
| wc -l

echo
echo "=========================================================="
echo "PARENT OF ZOMBIES"
echo "=========================================================="

ps -eo stat,pid,ppid \
| awk '$1 ~ /^Z/ {print $3}' \
| sort \
| uniq -c \
| sort -nr

echo
echo "=========================================================="
echo "OPEN FILES"
echo "=========================================================="

lsof 2>/dev/null \
| awk '{print $1}' \
| sort \
| uniq -c \
| sort -nr \
| head -30

echo
echo "=========================================================="
echo "PYTHON PROCESS"
echo "=========================================================="

pgrep -af python || true

echo
echo "=========================================================="
echo "VLLM"
echo "=========================================================="

pgrep -af vllm || true

echo
echo "=========================================================="
echo "QDRANT"
echo "=========================================================="

pgrep -af qdrant || true

echo
echo "=========================================================="
echo "DELBOT"
echo "=========================================================="

pgrep -af delbot || true

echo
echo "=========================================================="
echo "GPU"
echo "=========================================================="

nvidia-smi || true

echo
echo "=========================================================="
echo "CACHE"
echo "=========================================================="

grep -E "Cached|Buffers|Slab|SReclaimable|SUnreclaim" /proc/meminfo

echo
echo "=========================================================="
echo "DISK"
echo "=========================================================="

df -h

echo
echo "Largest Runtime"

du -sh runtime/* 2>/dev/null \
| sort -hr \
| head -30

echo
echo "Largest Workspace"

du -sh ./* 2>/dev/null \
| sort -hr \
| head -40

echo
echo "=========================================================="
echo "REPORT FINISHED"
echo "=========================================================="

echo "$REPORT"