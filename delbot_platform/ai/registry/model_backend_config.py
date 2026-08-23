from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelBackendConfig:

    dtype: str

    max_context: int

    tensor_parallel_size: int

    gpu_memory_utilization: float