#!/bin/bash
# ==============================================================================
# DELBOT ONE-CLICK SERVER LAUNCHER (CUSTOM PORT ISOLATION & AUTO-DB HEALTHCHECK)
# ==============================================================================

BACKEND_PORT=${BACKEND_PORT:-8008}
FRONTEND_PORT=${FRONTEND_PORT:-5178}

echo "=================================================="
echo "🚀 STARTING DELBOT SYSTEM ON GPU SERVER..."
echo "📡 Backend Port  : $BACKEND_PORT"
echo "🌐 Frontend Port : $FRONTEND_PORT"
echo "=================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "🔍 Checking GPU AI Model on port 11435..."
if curl -s http://127.0.0.1:11435/v1/models > /dev/null 2>&1; then
    echo "✅ GPU Model is ACTIVE on port 11435 (/workspace/Qwen3-30B-MoE)"
else
    echo "⚠️ GPU Model on port 11435 is not responding. Please ensure vLLM is running."
fi

echo "🔍 Checking Qdrant Vector Database on port 6333..."
if curl -s http://127.0.0.1:6333/dashboard > /dev/null 2>&1; then
    echo "✅ Qdrant Network Server is ACTIVE on port 6333"
else
    echo "⚙️ Starting Qdrant container..."
    docker start delbot_qdrant > /dev/null 2>&1 || docker compose up -d qdrant > /dev/null 2>&1 || true
    sleep 2
    if curl -s http://127.0.0.1:6333/dashboard > /dev/null 2>&1; then
        echo "✅ Qdrant started successfully on port 6333"
    else
        echo "ℹ️ Qdrant using embedded storage ($ROOT_DIR/qdrant_storage)"
        rm -f "$ROOT_DIR/qdrant_storage/.lock" 2>/dev/null || true
    fi
fi

echo "🧹 Cleaning up old instances on ports $BACKEND_PORT & $FRONTEND_PORT..."
fuser -k ${BACKEND_PORT}/tcp > /dev/null 2>&1 || true
fuser -k ${FRONTEND_PORT}/tcp > /dev/null 2>&1 || true
pkill -f "uvicorn delbot_platform.api.app:app --port $BACKEND_PORT" > /dev/null 2>&1 || true
pkill -f "serve -s dist -l $FRONTEND_PORT" > /dev/null 2>&1 || true
sleep 1

echo "⚙️ Starting Master Backend on port $BACKEND_PORT..."
nohup python3 -m uvicorn delbot_platform.api.app:app --host 0.0.0.0 --port $BACKEND_PORT > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID, Port: $BACKEND_PORT)"

echo "🌐 Starting Frontend Web on port $FRONTEND_PORT..."
cd "$ROOT_DIR/frontend"
nohup npx serve -s dist -l $FRONTEND_PORT > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID, Port: $FRONTEND_PORT)"
cd "$ROOT_DIR"

sleep 2

echo "=================================================="
echo "📊 VERIFYING SERVICES STATUS..."
echo "=================================================="
if curl -s http://127.0.0.1:${BACKEND_PORT}/health | grep -q "healthy"; then
    echo "✅ Master Backend : HEALTHY (http://127.0.0.1:${BACKEND_PORT})"
else
    echo "⚠️ Master Backend : Starting up... (check backend.log)"
fi

if curl -s -I http://127.0.0.1:${FRONTEND_PORT} | grep -q "200 OK"; then
    echo "✅ Frontend Web    : READY (http://127.0.0.1:${FRONTEND_PORT})"
else
    echo "⚠️ Frontend Web    : Starting up... (check frontend/frontend.log)"
fi

echo "=================================================="
echo "🎉 DELBOT IS NOW RUNNING ISOLATED ON PORTS ($BACKEND_PORT / $FRONTEND_PORT)!"
echo "=================================================="
