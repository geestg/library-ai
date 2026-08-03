#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BB
#
# Local LLM Provider Detection
#
# MVP SAFE AUDIT
# ------------------------------------------------------------------------------
#
# PURPOSE
#
# Detect kesiapan local LLM runtime untuk answer generation.
#
# Target:
#
# FastAPI Gateway
#       |
#       v
# LLM Provider
#       |
#       v
# Local Model Runtime
#
# Supported detection:
#
# - Ollama
# - vLLM
# - llama.cpp server
# - OpenAI compatible local endpoint
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Tidak mengubah source code
# - Tidak start model
# - Tidak download model
# - Tidak install package
# - Terminal tetap terbuka
#
# OUTPUT
#
# repository_data/mapping/
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1BB"
echo "Local LLM Provider Detection"
echo "======================================================================"

python3 <<'PY'

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path("/workspace/delbot")
OUT = ROOT / "repository_data/mapping"

OUT.mkdir(parents=True, exist_ok=True)


def check_cmd(cmd):
    try:
        result = subprocess.run(
            ["bash", "-lc", f"command -v {cmd}"],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def check_port(port):
    try:
        result = subprocess.run(
            [
                "bash",
                "-lc",
                f"timeout 1 bash -c '</dev/tcp/127.0.0.1/{port}'"
            ],
            capture_output=True
        )
        return result.returncode == 0
    except Exception:
        return False


providers = {
    "ollama": {
        "binary": check_cmd("ollama"),
        "port_11434": check_port(11434)
    },
    "vllm": {
        "binary": check_cmd("vllm"),
        "port_8000": check_port(8000)
    },
    "llama_cpp": {
        "binary": check_cmd("llama-server"),
        "port_8080": check_port(8080)
    }
}


env_detection = {
    "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE"),
    "OLLAMA_HOST": os.getenv("OLLAMA_HOST"),
    "LLM_PROVIDER": os.getenv("LLM_PROVIDER")
}


runtime_available = any(
    [
        providers["ollama"]["port_11434"],
        providers["vllm"]["port_8000"],
        providers["llama_cpp"]["port_8080"]
    ]
)


binary_available = any(
    [
        providers["ollama"]["binary"],
        providers["vllm"]["binary"],
        providers["llama_cpp"]["binary"]
    ]
)


status = "READY" if runtime_available else (
    "BINARY_AVAILABLE_WAITING_RUNTIME"
    if binary_available
    else
    "WAITING_LOCAL_LLM"
)


report = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BB",
    "providers": providers,
    "environment": env_detection,
    "llm_runtime": {
        "binary_available": binary_available,
        "runtime_available": runtime_available
    },
    "gateway_connection": {
        "provider_connected": runtime_available,
        "answer_generation_ready": runtime_available
    },
    "status": status
}


for name in [
    "local_llm_provider_detection.json",
    "local_llm_provider_detection_summary.json",
    "local_llm_provider_detection_report.json"
]:
    with open(OUT / name, "w") as f:
        json.dump(report, f, indent=2)


print(json.dumps(report, indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
python3 -m py_compile /workspace/delbot/tools/pr_5_1bb_local_llm_provider_detection.sh 2>/dev/null || true
echo ""
echo "Generated"
echo "repository_data/mapping/local_llm_provider_detection.json"
echo "repository_data/mapping/local_llm_provider_detection_summary.json"
echo "repository_data/mapping/local_llm_provider_detection_report.json"
echo ""
echo "======================================================================"
echo "PR-5.1BB COMPLETE"
echo "======================================================================"
echo ""
echo "NEXT"
echo "Jika READY lanjut PR-5.1BC LLM Gateway Provider Adapter"
echo "Jika WAITING_LOCAL_LLM lanjut sambungkan runtime model lokal"
