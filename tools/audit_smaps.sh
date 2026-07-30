#!/usr/bin/env bash
set -Eeuo pipefail

echo "====================================================="
echo "BIGGEST MEMORY MAPPING"
echo "====================================================="

for pid in $(ps -eo pid --sort=-rss | head -20 | tail -19)
do

if [ -f /proc/$pid/status ]; then

name=$(grep '^Name:' /proc/$pid/status | awk '{print $2}')

rss=$(grep '^VmRSS:' /proc/$pid/status)

peak=$(grep '^VmPeak:' /proc/$pid/status)

size=$(grep '^VmSize:' /proc/$pid/status)

echo
echo "PID : $pid"

echo "$name"

echo "$rss"

echo "$peak"

echo "$size"

fi

done
