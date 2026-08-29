#!/bin/bash
BACKEND_PORT=${BACKEND_PORT:-8008}
FRONTEND_PORT=${FRONTEND_PORT:-5178}
echo "🛑 STOPPING DELBOT SERVICES (Ports $BACKEND_PORT & $FRONTEND_PORT)..."
fuser -k ${BACKEND_PORT}/tcp > /dev/null 2>&1 || true
fuser -k ${FRONTEND_PORT}/tcp > /dev/null 2>&1 || true
pkill -f "uvicorn delbot_platform.api.app:app --port $BACKEND_PORT" > /dev/null 2>&1 || true
pkill -f "serve -s dist -l $FRONTEND_PORT" > /dev/null 2>&1 || true
echo "✅ Backend (Port $BACKEND_PORT) and Frontend (Port $FRONTEND_PORT) stopped cleanly."
