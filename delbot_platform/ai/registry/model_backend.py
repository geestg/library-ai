from __future__ import annotations

from enum import Enum


class ModelBackend(str, Enum):

    VLLM = "vllm"

    INFINITY = "infinity"

    NATIVE = "native"

    def __str__(self):

        return self.value