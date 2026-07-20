#!/bin/bash

echo "================================"
echo " DELBot Platform Health Check"
echo "================================"

echo

for p in 8100 8101 8104 8105 8106 8107 8200
do
    if ss -tulpn | grep -q ":$p "
    then
        echo "[OK] PORT $p"
    else
        echo "[FAIL] PORT $p"
    fi
done


echo
echo "================================"
echo " Runtime Health"
echo "================================"

echo

for url in \
"http://127.0.0.1:8100/health" \
"http://127.0.0.1:8101/health" \
"http://127.0.0.1:8104/health" \
"http://127.0.0.1:8105/health" \
"http://127.0.0.1:8106/health" \
"http://127.0.0.1:8107/health" \
"http://127.0.0.1:8200/"
do
    echo
    echo ">>> $url"
    curl -s "$url"
    echo
done
