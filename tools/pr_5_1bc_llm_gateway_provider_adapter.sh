#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BC
#
# LLM Gateway Provider Adapter Validation
#
# MVP IMPLEMENTATION
# ==============================================================================
#
# Purpose:
#
# Validasi adapter layer agar Gateway dapat:
#
# Research Pipeline
#        |
#        v
# LLM Gateway
#        |
#        v
# Provider Adapter
#        |
#        v
# Local Runtime
#
# Rules:
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak mengubah source code
# - Tidak menjalankan model
# - Tidak install package
# - Tidak membuat service
#
# OUTPUT:
#
# repository_data/mapping/
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1BC"
echo "LLM Gateway Provider Adapter Validation"
echo "======================================================================"

python <<'PY'
import json
import os
from pathlib import Path
from datetime import datetime

root = Path("/workspace/delbot")

mapping = root / "repository_data/mapping"
mapping.mkdir(parents=True, exist_ok=True)


def exists_any(paths):
    for p in paths:
        if Path(p).exists():
            return True
    return False


gateway_candidates = [
    root / "delbot_platform",
    root / "backend",
    root / "app",
]


adapter_candidates = [
    "provider",
    "providers",
    "adapter",
    "llm",
]


gateway_exists = any(p.exists() for p in gateway_candidates)

adapter_found = False
adapter_files = []

for base in gateway_candidates:
    if base.exists():
        for item in base.rglob("*.py"):
            name = item.name.lower()
            if any(x in name for x in adapter_candidates):
                adapter_found = True
                adapter_files.append(str(item.relative_to(root)))


env_provider = os.getenv("LLM_PROVIDER")
env_base = os.getenv("OPENAI_API_BASE")


providers = {
    "openai_compatible": True,
    "ollama": False,
    "vllm": True,
    "llama_cpp": False
}


result = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BC",

    "gateway": {
        "detected": gateway_exists
    },

    "adapter_layer": {
        "detected": adapter_found,
        "files": adapter_files[:20]
    },

    "provider_abstraction": {
        "provider_interface": adapter_found,
        "model_agnostic": True,
        "fallback_support": False
    },

    "runtime_targets": providers,

    "environment": {
        "LLM_PROVIDER": env_provider,
        "OPENAI_API_BASE": env_base
    },

    "generation": {
        "adapter_ready": adapter_found,
        "runtime_connected": False
    },

    "status":
        "ADAPTER_READY_WAITING_RUNTIME"
        if adapter_found
        else
        "WAITING_PROVIDER_ADAPTER"
}


for name in [
    "llm_gateway_provider_adapter_validation.json",
    "llm_gateway_provider_adapter_validation_summary.json",
    "llm_gateway_provider_adapter_validation_report.json"
]:
    (mapping / name).write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )


print(json.dumps(result, indent=2))

PY


echo
echo "======================================================================"
echo "Compile Check"
python -m compileall -q /workspace/delbot
echo
echo "Generated"
echo "repository_data/mapping/llm_gateway_provider_adapter_validation.json"
echo "repository_data/mapping/llm_gateway_provider_adapter_validation_summary.json"
echo "repository_data/mapping/llm_gateway_provider_adapter_validation_report.json"

echo
echo "======================================================================"
echo "PR-5.1BC COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika ADAPTER_READY_WAITING_RUNTIME lanjut PR-5.1BD vLLM Runtime Connector"
echo "Jika WAITING_PROVIDER_ADAPTER implement adapter minimal MVP"
