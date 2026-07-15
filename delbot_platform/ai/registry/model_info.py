from dataclasses import dataclass


@dataclass(slots=True)
class ModelInfo:

    name: str

    backend: str

    path: str

    port: int

    dtype: str

    max_context: int

    tensor_parallel_size: int

    gpu_memory_utilization: float