#!/bin/bash
# ==============================================================================
# DELBOT ONE-CLICK SERVER LAUNCHER
# ==============================================================================

echo "=================================================="
echo "🚀 STARTING DELBOT SYSTEM ON GPU SERVER..."
echo "=================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "🔍 Checking GPU AI Model on port 11435..."
if curl -s http://127.0.0.1:11435/v1/models > /dev/null 2>&1; then
    echo "✅ GPU Model is ACTIVE on port 11435 (/workspace/Qwen3-30B-MoE)"
else
    echo "⚠️ GPU Model on port 11435 is not responding. Please ensure vLLM is running."
fi

echo "🧹 Cleaning up old instances..."
pkill -f "uvicorn delbot_platform.api.app:app" > /dev/null 2>&1 || true
pkill -f "serve -s dist -l 5173" > /dev/null 2>&1 || true
sleep 1

echo "⚙️ Starting Master Backend on port 8000..."
nohup python3 -m uvicorn delbot_platform.api.app:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

echo "🌐 Starting Frontend Web on port 5173..."
cd "$ROOT_DIR/frontend"
nohup npx serve -s dist -l 5173 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"
cd "$ROOT_DIR"

sleep 2

echo "=================================================="
echo "📊 VERIFYING SERVICES STATUS..."
echo "=================================================="
if curl -s http://127.0.0.1:8000/health | grep -q "healthy"; then
    echo "✅ Master Backend : HEALTHY (http://127.0.0.1:8000)"
else
    echo "⚠️ Master Backend : Starting up... (check backend.log)"
fi

if curl -s -I http://127.0.0.1:5173 | grep -q "200 OK"; then
    echo "✅ Frontend Web    : READY (http://127.0.0.1:5173)"
else
    echo "⚠️ Frontend Web    : Starting up... (check frontend/frontend.log)"
fi

echo "=================================================="
echo "🎉 DELBOT IS NOW RUNNING ON GPU SERVER!"
echo "=================================================="
