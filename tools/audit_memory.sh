#!/usr/bin/env bash
set -Eeuo pipefail

echo "=============================================================="
echo " DELBOT MEMORY AUDIT"
echo "=============================================================="

echo
echo "HOST"
hostname

echo
echo "UPTIME"
uptime

echo
echo "FREE"
free -h

echo
echo "--------------------------------------------------------------"
echo "TOP 40 PROCESS RSS"
echo "--------------------------------------------------------------"

ps -eo \
pid,\
ppid,\
user,\
rss,\
vsz,\
%mem,\
%cpu,\
etime,\
cmd \
--sort=-rss \
| head -40

echo
echo "--------------------------------------------------------------"
echo "TOP PYTHON"
echo "--------------------------------------------------------------"

ps -eo \
pid,\
ppid,\
rss,\
%mem,\
etime,\
cmd \
| grep python \
| grep -v grep \
| sort -nr -k3 \
| head -50

echo
echo "--------------------------------------------------------------"
echo "TOP VLLM"
echo "--------------------------------------------------------------"

ps -eo \
pid,\
ppid,\
rss,\
%mem,\
etime,\
cmd \
| grep vllm \
| grep -v grep

echo
echo "--------------------------------------------------------------"
echo "TOP QDRANT"
echo "--------------------------------------------------------------"

ps -eo \
pid,\
ppid,\
rss,\
%mem,\
etime,\
cmd \
| grep qdrant \
| grep -v grep

echo
echo "--------------------------------------------------------------"
echo "TOP DELBOT"
echo "--------------------------------------------------------------"

ps -eo \
pid,\
ppid,\
rss,\
%mem,\
etime,\
cmd \
| grep delbot_platform \
| grep -v grep

echo
echo "--------------------------------------------------------------"
echo "MEMORY MAP"
echo "--------------------------------------------------------------"

cat /proc/meminfo

echo
echo "--------------------------------------------------------------"
echo "SLAB"
echo "--------------------------------------------------------------"

grep -E "Slab|SReclaimable|SUnreclaim|KernelStack|PageTables" /proc/meminfo

echo
echo "--------------------------------------------------------------"
echo "ZOMBIE"
echo "--------------------------------------------------------------"

ps -eo stat,pid,ppid,cmd | awk '$1 ~ /^Z/'

echo
echo "TOTAL ZOMBIE"

ps -eo stat | grep -c '^Z'

echo
echo "DONE"
