#!/bin/bash

echo "=== CHAT ==="
curl -s http://127.0.0.1:8101/health
echo


echo "=== EMBEDDING ==="
curl -s http://127.0.0.1:8105/health
echo


echo "=== RERANKER ==="
curl -s http://127.0.0.1:8106/health
echo


echo "=== VISION ==="
curl -s http://127.0.0.1:8104/health
echo


echo "=== OCR ==="
curl -s http://127.0.0.1:8107/health
echo
