#!/bin/bash
# ==============================================================================
# DELBOT ALL-IN-ONE MASTER LAUNCHER (MODELS + BACKEND + FRONTEND)
# ==============================================================================

echo "=========================================================="
echo "🚀 MENYALAKAN SELURUH SISTEM DELBOT (AI + BACKEND + WEB)..."
echo "=========================================================="

# 1. Pastikan Virtual Environment vLLM aktif
if [ -d "/workspace/vllm_env" ]; then
    source /workspace/vllm_env/bin/activate
fi

# 2. Nyalakan Model LLM (Llama 3.3 70B di Port 11436) jika belum jalan
if curl -s http://127.0.0.1:11436/v1/models > /dev/null 2>&1; then
    echo "✅ [1/4] Model Llama 3.3 70B (Port 11436) SUDAH AKTIF."
else
    echo "⚡ [1/4] Menyalakan Model Llama 3.3 70B (Port 11436)..."
    nohup python3 -m vllm.entrypoints.openai.api_server \
        --model meta-llama/Llama-3.3-70B-Instruct \
        --host 0.0.0.0 \
        --port 11436 \
        --gpu-memory-utilization 0.70 > /workspace/slm_11436.log 2>&1 &
fi

# 3. Nyalakan Model LLM MoE Sekunder di Port 11435 jika ada
if curl -s http://127.0.0.1:11435/v1/models > /dev/null 2>&1; then
    echo "✅ [2/4] Model MoE Sekunder (Port 11435) SUDAH AKTIF."
else
    echo "ℹ️ [2/4] Port 11435 (MoE Sekunder) tidak aktif. DELBot fokus menggunakan Llama 3.3 70B di Port 11436."
fi

# 4. Nyalakan Master Backend (Port 8000)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
pkill -f "uvicorn delbot_platform.api.app:app" > /dev/null 2>&1 || true
echo "⚙️ [3/4] Menyalakan Master Backend (Port 8000)..."
nohup python3 -m uvicorn delbot_platform.api.app:app --host 0.0.0.0 --port 8000 > "$ROOT_DIR/backend.log" 2>&1 &

# 5. Nyalakan Frontend Web (Port 5173)
cd "$ROOT_DIR/frontend"
pkill -f "serve -s dist -l 5173" > /dev/null 2>&1 || true
echo "🌐 [4/4] Menyalakan Frontend Web (Port 5173)..."
nohup npx serve -s dist -l 5173 > "$ROOT_DIR/frontend/frontend.log" 2>&1 &
cd "$ROOT_DIR"

sleep 3

echo "=========================================================="
echo "🎉 SELURUH SISTEM SELESAI DINYALAKAN OTOMATIS!"
echo "• Primary LLM (Llama 3.3 70B): Port 11436"
echo "• Master Backend API          : Port 8000"
echo "• Frontend Web (UI)           : Port 5173"
echo "=========================================================="

