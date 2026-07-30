#!/usr/bin/env bash
set -e

echo "====================================================="
echo "DELBOT DEEP MEMORY AUDIT"
echo "====================================================="
echo

echo "========== HOST =========="
hostname
echo

echo "========== DATE =========="
date
echo

echo "========== UPTIME =========="
uptime
echo

echo "========== FREE =========="
free -h
echo

echo "========== MEMINFO =========="
grep -E \
'MemTotal|MemFree|MemAvailable|Buffers|Cached|Slab|SReclaimable|SUnreclaim|PageTables|KernelStack|AnonPages|Shmem|Mapped|CommitLimit|Committed_AS|HugePages|AnonHugePages' \
/proc/meminfo

echo
echo "====================================================="
echo "TOP ANON RSS"
echo "====================================================="

ps -eo pid,user,rss,cmd \
| sort -k3 -nr \
| head -80

echo
echo "====================================================="
echo "PROCESS VM SIZE"
echo "====================================================="

for pid in $(ls /proc | grep '^[0-9]' | sort -n)
do
    if [[ -r /proc/$pid/status ]]; then

        rss=$(grep VmRSS /proc/$pid/status 2>/dev/null | awk '{print $2}')
        size=$(grep VmSize /proc/$pid/status 2>/dev/null | awk '{print $2}')
        peak=$(grep VmPeak /proc/$pid/status 2>/dev/null | awk '{print $2}')

        [[ -z "$rss" ]] && rss=0
        [[ -z "$size" ]] && size=0
        [[ -z "$peak" ]] && peak=0

        cmd=$(tr '\0' ' ' </proc/$pid/cmdline)

        [[ -z "$cmd" ]] && continue

        printf "%12d %12d %12d %12d %s\n" \
            "$rss" \
            "$size" \
            "$peak" \
            "$pid" \
            "$cmd"

    fi
done | sort -nr | head -60

echo
echo "====================================================="
echo "SHMEM"
echo "====================================================="

df -h | grep shm || true

echo

mount | grep shm || true

echo
echo "====================================================="
echo "TMPFS"
echo "====================================================="

mount | grep tmpfs

echo
echo "====================================================="
echo "CGROUP"
echo "====================================================="

cat /proc/self/cgroup

echo
echo "====================================================="
echo "CGROUP MEMORY"
echo "====================================================="

find /sys/fs/cgroup \
-name memory.current \
-exec sh -c '
for f
do
echo
echo "$f"
cat "$f"
done
' sh {} \; 2>/dev/null

echo
echo "====================================================="
echo "MEMORY.MAX"
echo "====================================================="

find /sys/fs/cgroup \
-name memory.max \
-exec sh -c '
for f
do
echo
echo "$f"
cat "$f"
done
' sh {} \; 2>/dev/null

echo
echo "====================================================="
echo "MEMORY.STAT"
echo "====================================================="

find /sys/fs/cgroup \
-name memory.stat \
-exec sh -c '
for f
do
echo
echo "$f"
cat "$f"
done
' sh {} \; 2>/dev/null

echo
echo "====================================================="
echo "LARGEST OPEN FILES"
echo "====================================================="

for pid in $(ls /proc | grep '^[0-9]')
do
    if [[ -d /proc/$pid/fd ]]; then
        count=$(ls /proc/$pid/fd 2>/dev/null | wc -l)
        cmd=$(tr '\0' ' ' </proc/$pid/cmdline)
        [[ -z "$cmd" ]] && continue
        printf "%8d %8d %s\n" "$count" "$pid" "$cmd"
    fi
done | sort -nr | head -40

echo
echo "====================================================="
echo "SYSTEMD"
echo "====================================================="

systemctl --failed 2>/dev/null || true

echo
echo "====================================================="
echo "DONE"
echo "====================================================="
