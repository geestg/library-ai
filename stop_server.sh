#!/bin/bash
echo "🛑 STOPPING DELBOT SERVICES..."
pkill -f "uvicorn delbot_platform.api.app:app" > /dev/null 2>&1 || true
pkill -f "serve -s dist -l 5173" > /dev/null 2>&1 || true
echo "✅ Backend and Frontend stopped cleanly."
